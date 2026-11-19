#!/usr/bin/env python3
"""Held-out first-token ranking diagnostic for eSonde v8.

No target response token is provided to candidate proposal, P activation, R
activation, or Obsiss scoring. The target token is read only after all candidate
rankings have been computed, for evaluation. This is a constrained one-step
ranking experiment, not free-response generation and not a quality proof.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta
import hashlib
import json
from pathlib import Path
import sys
import time


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def now_local() -> str:
    return datetime.now(timezone(timedelta(hours=1))).isoformat(timespec="seconds")


def first_token(text: str, tokenize) -> str | None:
    tokens = tokenize(text)
    return str(tokens[0]).casefold() if tokens else None


def deterministic_sample(rows: list[dict], per_language: int, langs: list[str]) -> list[dict]:
    picked = []
    for lang in langs:
        candidates = [r for r in rows if str(r.get("lang", "")).casefold() == lang.casefold()]
        candidates.sort(key=lambda r: hashlib.sha256(
            (str(r.get("source_tree_id_sha256", "")) + "\0" +
             str(r.get("source_target_message_id_sha256", ""))).encode("utf-8")
        ).hexdigest())
        picked.extend(candidates[:per_language])
    return picked


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--model-dir", type=Path, required=True)
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--test-jsonl", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--trace-dir", type=Path, required=True)
    parser.add_argument("--obsiss", type=int, default=256)
    parser.add_argument("--per-language", type=int, default=2)
    parser.add_argument("--candidate-limit", type=int, default=16)
    parser.add_argument("--languages", default="en,es,fr,de,ru,zh")
    args = parser.parse_args()

    ws = args.workspace.resolve()
    model_dir = args.model_dir.resolve()
    profile_path = args.profile.resolve()
    test_path = args.test_jsonl.resolve()
    output_path = args.output.resolve()
    trace_dir = args.trace_dir.resolve()

    sys.path.insert(0, str((ws / "Dmodel_eSonde_v8" / "src").resolve()))
    from esonde_v6.model import load_model
    from esonde_v6.features import tokenize
    from esonde_v7.generation import (
        _anchor_maps, _propose_candidates, _candidate_records,
        classify_dialogue_intent,
    )
    from esonde_v7.activation import activate_convergent_text, activate_text
    from esonde_v7.observers import ObsissPopulation
    from esonde_v6.generation import select_language_statistics, prepare_statistics
    from esonde_v7.context import DialogueContext
    from esonde_v8.dialogue_learning import load_profiles, profile_context_evidence, \
        profile_evidence_from_context, proposal_items

    started = time.perf_counter()
    model = load_model(model_dir, n_obsiss=args.obsiss, verify=True)
    profile_payload = load_profiles(profile_path)
    profile = profile_payload["profiles"]["everyday_dialogue"]
    raw_rows = [json.loads(line) for line in test_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    languages = [x.strip() for x in args.languages.split(",") if x.strip()]
    sample = deterministic_sample(raw_rows, args.per_language, languages)
    if not sample:
        raise RuntimeError("deterministic test sample is empty")

    sensitivity = (model.metadata["obsiss"].get("epsilon_numerator", 1) /
                   model.metadata["obsiss"].get("epsilon_denominator", 10))
    configs = [
        ("historical_v7", {}),
        ("no_own_context", {"context_strength": 0.0}),
        ("no_cross_observation", {"cross_observation_strength": 0.0}),
        ("no_context_no_cross", {"context_strength": 0.0, "cross_observation_strength": 0.0}),
        ("identity_cross_permutation", {"cross_permutation": tuple(range(16))}),
    ]
    populations = {
        name: ObsissPopulation(model.weights, model.metadata["weights"]["sha256"],
                               sensitivity_strength=sensitivity, **kwargs)
        for name, kwargs in configs
    }

    per_example = []
    aggregate = {name: {"hits": 0, "mrr_sum": 0.0, "n": 0, "top1": Counter()}
                 for name, _ in configs}
    language_routes = Counter()
    source_counts = Counter()
    ngram_route_counts = Counter()

    for index, row in enumerate(sample, 1):
        prompt = str(row.get("context", "")).strip()
        response = str(row.get("response", ""))
        target = first_token(response, tokenize)
        if not prompt or not target:
            continue

        # Candidate proposal uses only prompt/context and TRAIN-derived model stats.
        context = DialogueContext([], prompt)
        combined_context = context.all_text(include_prefix=False)
        language_stats, language_selection = select_language_statistics(model.stats, combined_context)
        prepare_statistics(language_stats)
        route = str(language_selection.get("selected", "global"))
        language_routes[route] += 1
        profile_context = profile_context_evidence(
            profile, prompt, "everyday_dialogue", history=None,
            language_route=route, allowed_tokens=language_stats.get("unigrams", {}).keys())
        profile_evidence = profile_evidence_from_context(profile_context, profile, prefix=[])
        profile_items = proposal_items(profile_evidence)
        prompt_terms, dialogue_terms, _ = _anchor_maps(context, prompt, language_stats)
        intent = classify_dialogue_intent(prompt)
        intent["language"] = route.casefold()
        intent["_prompt_text"] = prompt
        occurrence_terms = context.weighted_terms_by_role()["prompt"]
        nexts = _propose_candidates(
            language_stats, [], prompt_terms, dialogue_terms, {}, False,
            args.candidate_limit, dialogue_intent=intent,
            prompt_occurrence_terms=occurrence_terms, profile_items=profile_items)
        records = _candidate_records(
            language_stats, context, prompt, [], nexts, {}, False,
            language=route, profile_evidence=profile_evidence,
            dialogue_learning_module=__import__("esonde_v8.dialogue_learning", fromlist=["x"]))
        tokens = [str(r["token"]).casefold() for r in records]
        if not records:
            continue
        for r in records:
            source_counts[str(r.get("proposal_source", "unknown"))] += 1

        # P is produced by the same convergent initializer used by chat runtime.
        p_obs = activate_convergent_text(
            model, prompt, "P", trace_dir, active_count=args.obsiss, keep_trace=False)
        phases = list(p_obs.cycle_q_contexts or [p_obs.q_context])
        phases = [q for q in phases if q is not None]
        if not phases:
            raise RuntimeError("P activation returned no q-context phase")

        # The target response is not used here. Only the candidate token is fed to
        # R, paired with each P phase; all five ablations share these exact states.
        phase_pair_matrices = []
        for phase_q in phases:
            columns = []
            for record in records:
                r_obs = activate_text(
                    model, str(record["token"]), "R", trace_dir,
                    q_context=phase_q, keep_trace=False, active_count=args.obsiss)
                columns.append(populations["historical_v7"].pair_score_vector(
                    phase_q, r_obs.published, args.obsiss))
                del r_obs
            phase_pair_matrices.append(populations["historical_v7"].pair_score_matrix(columns))

        per_variant = {}
        for name, population in populations.items():
            phase_scores = defaultdict(list)
            convergence = []
            for phase_q, pair_matrix in zip(phases, phase_pair_matrices):
                judged = population.evaluate(records, phase_q, active_count=args.obsiss,
                                             top_k=5, response_pair_scores=pair_matrix)
                convergence.append(judged.get("convergence", {}))
                for ranked in judged.get("ranked", []):
                    phase_scores[str(ranked["token"]).casefold()].append(
                        float(ranked["collective_rank_score"]))
            means = {token: sum(vals) / len(vals) for token, vals in phase_scores.items()}
            order = sorted(means, key=lambda token: (-means[token], token))
            try:
                rank = order.index(target) + 1
            except ValueError:
                rank = None
            rr = 1.0 / rank if rank else 0.0
            hit5 = bool(rank and rank <= 5)
            per_variant[name] = {
                "target_rank": rank,
                "target_in_candidate_pool": rank is not None,
                "reciprocal_rank": rr,
                "hit_at_5": hit5,
                "top1": order[0] if order else None,
                "top5": order[:5],
                "mean_rank_scores": means,
                "phase_count": len(phases),
                "partition_stability_each_phase": convergence,
                "observer_configuration_id": population.population_sha256,
            }
            aggregate[name]["n"] += 1
            aggregate[name]["hits"] += int(hit5)
            aggregate[name]["mrr_sum"] += rr
            aggregate[name]["top1"][order[0] if order else "<empty>"] += 1

        per_example.append({
            "sample_index": index,
            "source_language": row.get("lang"),
            "language_route": route,
            "language_route_status": language_selection.get("status"),
            "source_tree_id_sha256": row.get("source_tree_id_sha256"),
            "source_target_message_id_sha256": row.get("source_target_message_id_sha256"),
            "context_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
            "target_first_token": target,
            "candidate_count": len(records),
            "candidate_tokens": tokens,
            "candidate_sources": [r.get("proposal_source") for r in records],
            "p_activation": p_obs.stats,
            "variants": per_variant,
        })
        print(f"[{index}/{len(sample)}] lang={row.get('lang')} route={route} candidates={len(records)} "
              f"target_covered={per_variant['historical_v7']['target_in_candidate_pool']} "
              f"baseline_rank={per_variant['historical_v7']['target_rank']}", flush=True)

    summary = {}
    for name, values in aggregate.items():
        n = values["n"]
        summary[name] = {
            "n": n,
            "candidate_pool_recall": values["hits"] / n if n else 0.0,
            "mrr": values["mrr_sum"] / n if n else 0.0,
            "top1_frequency": dict(values["top1"]),
        }

    payload = {
        "schema": "esonde.v8.heldout_next_token_rank_diagnostic.v1",
        "created_local": now_local(),
        "experiment_id": "V8-P0-OBSISS-HELDOUT-NEXT-TOKEN-001",
        "status": "COMPLETED_COMPONENT_DIAGNOSTIC" if per_example else "NO_USABLE_EXAMPLES",
        "task": "prompt-to-first-response-token candidate ranking only; no full answer generation",
        "non_response_enabled": False,
        "test_split_only": True,
        "target_used_during_candidate_proposal_or_scoring": False,
        "target_access_stage": "post-ranking metric calculation only",
        "data": {
            "path": str(test_path), "sha256": sha256(test_path),
            "source_split": "OpenAssistant/oasst1 validation reserved as held-out test",
            "sample_count_requested": len(sample), "sample_count_evaluated": len(per_example),
            "per_language_requested": args.per_language, "languages": languages,
            "language_routes": dict(language_routes),
        },
        "model": {
            "checkpoint_sha256": model.metadata["weights"]["sha256"],
            "profile_sha256": sha256(profile_path),
            "profile_training_examples": profile.get("training_examples"),
            "neural_components": [], "obsiss_active_count": args.obsiss,
            "dimension": model.weights.dimension,
            "candidate_limit": args.candidate_limit,
        },
        "variants": {
            "historical_v7": "context_strength=0.5; cross_strength=0.25; historical permutation; scale=8192",
            "no_own_context": "context_strength=0; cross_strength=0.25",
            "no_cross_observation": "context_strength=0.5; cross_strength=0",
            "no_context_no_cross": "context_strength=0; cross_strength=0",
            "identity_cross_permutation": "context_strength=0.5; cross_strength=0.25; identity permutation",
        },
        "aggregate": summary,
        "proposal_source_counts": dict(source_counts),
        "examples": per_example,
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "interpretation_constraints": [
            "This diagnostic evaluates only the first response token, not complete answer coherence.",
            "Candidate-pool recall and conditional rank are reported separately.",
            "A low recall is a proposal-coverage limitation, not evidence about Obsiss ranking.",
            "Internal partition stability is not truth, relevance, or generalization.",
            "Only the first 256 checkpoint rows were used; this is not a full-population result.",
            "Language route is inferred from prompt text; source lang is metadata and is not supplied to the model.",
        ],
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "output": str(output_path),
                      "sha256": sha256(output_path), "aggregate": summary,
                      "elapsed_seconds": payload["elapsed_seconds"]}, ensure_ascii=False), flush=True)
    return 0 if per_example else 2


if __name__ == "__main__":
    raise SystemExit(main())
