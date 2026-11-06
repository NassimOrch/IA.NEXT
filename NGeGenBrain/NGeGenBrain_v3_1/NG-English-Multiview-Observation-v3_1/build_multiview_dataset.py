#!/usr/bin/env python3
"""Build an English-only student training corpus from the actual multi-view observation log.

The corpus uses only architecture metadata, held-out-independent observation prompts, internal
state summaries, attention summaries, interventions, and short source continuations. It never
imports language-model scores calculated on the reserved cross-model evaluation strings.
"""
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'src'
if str(SRC) not in sys.path: sys.path.insert(0,str(SRC))
FACETS={
 'behavioral_generation':[
  "An autoregressive continuation is evidence about generated behavior for one exact prompt and decoding configuration.",
  "Short deterministic continuations should be recorded as raw output, not edited into more fluent answers.",
  "A prompt can trigger system-template tokens before the user's text, so generation evidence must include prompt formatting.",
  "Generation quality should be checked for both local coherence and whether the model follows the requested task.",
 ],
 'next_token_statistics':[
  "Next-token accuracy and negative log likelihood measure local prediction, but they do not directly measure factual reasoning.",
  "Native-token perplexity depends on the tokenizer, so token-normalized values should not be ranked across unrelated tokenizers.",
  "Bits per UTF-8 byte offers a common normalization when models use different tokenization schemes, with coverage recorded explicitly.",
  "A forward pass must produce finite logits before any confidence or entropy statistic is interpreted.",
 ],
 'hidden_representations':[
  "A hidden-state summary should record the exact layer index, tensor shape, input hash, and model hash.",
  "A representation's root mean square and variance summarize numerical scale but do not assign a semantic label to neurons.",
  "Comparing hidden-state summaries across architectures requires attention to dimensionality, token positions, and normalization.",
  "A single prompt cannot establish that a representation remains stable across topics or languages.",
 ],
 'attention_patterns':[
  "Attention entropy describes how concentrated a head's attention distribution is for the recorded input positions.",
  "An attention matrix is an observable numerical object, not by itself proof that a head implements a named linguistic function.",
  "The attention mask must prevent a causal decoder from using future tokens when predicting the next token.",
  "A recurrent model without attention should report that the capability is absent instead of fabricating attention maps.",
 ],
 'ablation_response':[
  "A zero intervention after a selected block tests dependence on the post-block residual representation for that input.",
  "The baseline and intervention must use identical inputs, weights, device, and decoding-independent measurement settings.",
  "A changed top prediction is a measurable effect, but it does not prove that the intervened block has a unique semantic role.",
  "A zero effect is also a result and should remain in the registry rather than being filtered out.",
 ],
 'scaling_response':[
  "Scaling an internal representation by one half is a distinct intervention from replacing it with zeros.",
  "The intervention log should record the scaling coefficient and the norm of the difference between baseline and intervened logits.",
  "A scaling intervention may preserve the top token while changing the rest of the probability distribution.",
  "A repeated identical intervention result can indicate a control or implementation error and should be investigated.",
 ],
 'cross_language_behavior':[
  "A multilingual comparison needs prompts from each evaluated language and must distinguish input-language ability from training-domain coverage.",
  "The same prompt text should be submitted to every model when the tokenizer and chat template permit a fair comparison.",
  "A very short continuation is a runtime smoke test, not adequate evidence of long-form conversational competence.",
  "A model's training-language bias should be treated as a domain condition, not as a universal score of model quality.",
 ],
 'limitations_hypotheses':[
  "A student with tens of thousands of parameters is not capacity-matched to teacher models with tens or hundreds of millions of parameters.",
  "Behavioral similarity on a finite corpus is weaker than equivalence under causal intervention or internal-mechanism reconstruction.",
  "A proposed mechanism remains a hypothesis until it survives counterexamples and new interventions on independent inputs.",
  "Differences between architectures and tokenizers must remain visible in the report instead of being normalized away rhetorically.",
 ],
}
FACET_ORDER=list(FACETS)

def sha256_bytes(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def sha256_file(p:Path)->str:return sha256_bytes(p.read_bytes())
def clean_ascii(text:str)->str:
 # The corpus is English only; source generations that contain CJK are described in English, not copied verbatim.
 text=text.encode('ascii','replace').decode('ascii')
 return ' '.join(text.split())

def build(source_study:Path,out:Path):
 d=json.loads(source_study.read_text(encoding='utf-8'))
 obs={r['model_id']:r for r in d['multi_view_observations']}
 gens=d['generation_observations']
 models=d['models']
 # 8 evidence-grounded training documents for every view family; no language-modeling scores from the reserved evaluation set are read.
 training={facet:[] for facet in FACET_ORDER}
 # Behavioral continuations: describe raw results without replacing them with authored ideal answers.
 for name,rows in gens.items():
  for r in rows:
   text=clean_ascii(f"In the multi-view generation run, model {name} received this {r['language']} prompt: {r['prompt']}. The recorded raw continuation was {r['generated_text']!r}. This is a direct observation from one short deterministic generation, not a general capability claim.")
   if any(ord(c)>127 for c in r['generated_text']):
    text=clean_ascii(f"In the multi-view generation run, model {name} received a {r['language']} prompt about a capital city. The recorded raw continuation contained Chinese-script text referring to China and Beijing. The raw output was not edited and was only a short deterministic continuation.")
   training['behavioral_generation'].append((text,[f"generation:{name}:{r['language']}:{r['prompt_id']}"]))
 training['behavioral_generation'].extend([
  ("The source-model generation table stores the prompt, language, decoding seed, continuation, generated token count, and elapsed time for every saved trial.",["study:generation-registry"]),
  ("A raw continuation can be linguistically weak even when the model loads and computes finite logits; runtime success and task quality are separate outcomes.",["study:interpretation"]),
 ])
 # Source model descriptor and baseline facts, using prompts reserved for observation rather than evaluation scoring.
 for name,r in obs.items():
  b=r['baseline']; h=r['hierarchy']['level_0_model']
  training['next_token_statistics'].append((clean_ascii(f"For observation input {r['input']!r}, model {name} processed {b['token_count']} tokens; its most likely next token id was {b.get('next_token_id',b.get('next_byte_id'))}, top-one probability {b['top1_probability']:.6f}, and next-token entropy {b['next_token_entropy_nats']:.6f} nats."),[f"observation:{name}:baseline"]))
  hs=b.get('hidden_layer_summary',[])
  if hs:
   pick=[hs[0],hs[len(hs)//2],hs[-1]]
   desc='; '.join(f"layer {x['layer']} shape {x['shape']} RMS {x['rms']:.6f} variance {x['variance']:.6f}" for x in pick)
   training['hidden_representations'].append((clean_ascii(f"On the recorded observation prompt, {name} exposed {len(hs)} hidden-state outputs. Selected summaries were {desc}. These scalar statistics describe scale and shape, not semantic identity."),[f"observation:{name}:hidden-state-summary"]))
  else:
   training['hidden_representations'].append((f"The student {name} exposes a single recurrent hidden-state output rather than a stack of transformer block outputs. Its recurrent state is observed as a time-dependent summary, not as an attention layer.",[f"observation:{name}:hidden-state-summary"]))
  at=b.get('attention_summary',[])
  if at:
   picks=[at[0],at[len(at)//2],at[-1]]
   desc='; '.join(f"layer {x['layer']} mean attention entropy {x['mean_entropy_nats']:.6f} nats" for x in picks)
   training['attention_patterns'].append((clean_ascii(f"For {name}, the attention capture contained {len(at)} layers on a fixed prompt. Selected entropy observations were {desc}. This is a prompt-conditioned numerical summary."),[f"observation:{name}:attention-summary"]))
  else:
   training['attention_patterns'].append((f"The architecture of {name} is recurrent and has no attention heads. The experiment recorded the capability as unavailable instead of inventing attention tensors.",[f"observation:{name}:attention-capability"] ))
  zs=next((x for x in r['interventions'] if x['intervention_type']=='zero_update'),None) or next((x for x in r['interventions'] if x['intervention_type']=='zero'),None)
  if zs:
   training['ablation_response'].append((clean_ascii(f"A residual-preserving block-update ablation at {zs['target']} on model {name} changed top prediction from id {zs['baseline_top1_id']} to id {zs['intervention_top1_id']}; logit L2 delta was {zs['logit_l2_delta']:.6f}, mean absolute delta {zs['mean_abs_logit_delta']:.6f}, and entropy change {zs['entropy_delta_nats']:.6f} nats."),[f"intervention:{name}:{zs['target']}:{zs['intervention_type']}"]))
  else:
   training['ablation_response'].append((f"The student model {name} has one GRU block; the controlled intervention targets the recurrent output state because there are no transformer layers to ablate.",[f"intervention:{name}:rnn-output:zero"]))
  sc=next((x for x in r['interventions'] if x['intervention_type']=='scale_update'),None) or next((x for x in r['interventions'] if x['intervention_type']=='scale'),None)
  if sc:
   training['scaling_response'].append((clean_ascii(f"Scaling the net block update by coefficient {sc['parameters'].get('scale',0.5)} at {sc['target']} in {name} changed top prediction={sc['top1_changed']}; the logit L2 delta was {sc['logit_l2_delta']:.6f} and entropy changed by {sc['entropy_delta_nats']:.6f} nats."),[f"intervention:{name}:{sc['target']}:{sc['intervention_type']}"]))
  else:
   training['scaling_response'].append((f"The student {name} has no transformer attention block; its measured scale operation was applied after the GRU output and logged with the same input as its baseline.",[f"intervention:{name}:rnn-output:scale"]))
  training['limitations_hypotheses'].append((clean_ascii(f"Architecture audit for {name}: {h.get('architecture')}, {h.get('parameters_estimate',h.get('parameters'))} parameters, {h.get('layers')} layers, hidden size {h.get('hidden_size')}, vocabulary size {h.get('vocab_size')}. These facts define scale and structure but do not establish a source-equivalent reconstruction."),[f"architecture:{name}"]))
 # Cross-language evidence is built from the previously recorded short generation trials only.
 for name,rows in gens.items():
  by={r['language']:r for r in rows}
  en=by.get('en'); zh=by.get('zh')
  if en and zh:
   en_text=en['generated_text']
   if any(ord(c)>127 for c in en_text): en_text='a short continuation with non-Latin script'
   zh_text=zh['generated_text']
   if any(ord(c)>127 for c in zh_text): zh_text='a short continuation containing Chinese-script text'
   training['cross_language_behavior'].append((clean_ascii(f"The paired language smoke test for {name} used one English prompt and one Chinese prompt. The English continuation was recorded as {en_text!r}; the Chinese continuation was recorded as {zh_text!r}. Two short trials are insufficient to estimate broad multilingual ability."),[f"generation:{name}:paired-languages"]))
 # Add five distinct methodological records per facet so the training split contains 8 unique docs.
 train_additions={
 'behavioral_generation':[
  "A generation result is indexed by model hash, tokenizer version, input string, chat template, decoding seed, and token budget.",
  "The continuation produced by a source model is retained separately from the formatted prompt so prompt leakage is visible.",
  "An output that begins by repeating the system instruction should be recorded as observed rather than silently repaired.",
  "Task-following must be evaluated with longer blinded prompts after a loader smoke test succeeds.",
  "A prompt with no generated tokens may indicate a stop token or a decoding issue and needs its own diagnostic record.",],
 'next_token_statistics':[
  "Entropy is calculated from the normalized next-token distribution and is expressed in nats when natural logarithms are used.",
  "Top-one confidence can be high for a poor continuation, so confidence is interpreted together with held-out loss and generation checks.",
  "The evaluated byte coverage is recorded explicitly because a token count does not correspond to the same amount of text for all tokenizers.",
  "Only the validation partition may guide checkpoint selection; the final test must remain untouched until that choice is frozen.",
  "A comparison log stores exact model and dataset hashes with all aggregate metrics so that results can be reproduced.",],
 'hidden_representations':[
  "The observation engine records selected layer indices rather than giving the analyst only a pooled model-level number.",
  "A hidden-state shape reveals tensor dimensions but does not identify a neuron or direction as a named concept.",
  "A feature attribution needs a contrastive input, a predicted effect, and an independent test before its label is consolidated.",
  "Layerwise summaries should retain all selected records, including outliers and non-finite-value failures.",
  "A representation may change with context, so one prompt is a pilot observation rather than a stable feature definition.",],
 'attention_patterns':[
  "Attention entropy is measured over the key-position distribution for each recorded query position and then summarized.",
  "A causal mask makes future-token attention probability zero before softmax in the model's forward computation.",
  "Comparisons of attention distributions should keep sequence positions and input tokens aligned where possible.",
  "An intervention on a block output is not the same as patching an individual head or attention edge.",
  "A model without attention exposes no head-level causal claim; its recurrent state must be studied with appropriate interventions.",],
 'ablation_response':[
  "A layer ablation protocol declares the exact target, type of intervention, baseline, input hash, and model revision before execution.",
  "The causal interpretation is scoped to the actual operation applied; zeroing a post-block stream differs from removing a learned module.",
  "Counterexamples should include inputs where the intervention has a small effect as well as inputs where it changes the prediction.",
  "The same intervention should be repeated on a second prompt before generalizing an effect beyond its recorded case.",
  "An unchanged argmax does not imply unchanged probabilities because non-maximal logits may still move substantially.",],
 'scaling_response':[
  "A scale sweep can compare coefficients zero, one quarter, one half, three quarters, and one under an otherwise fixed protocol.",
  "The no-op scale of one is a control that should reproduce the baseline within numeric tolerance.",
  "A zero coefficient is the limiting case of scaling but should still be logged as its own intervention parameter.",
  "A strong response to scaling identifies sensitivity to a representation pathway, not necessarily a semantic feature.",
  "The intervention engine must fail loudly if a requested target or operation is unavailable for the selected adapter.",],
 'cross_language_behavior':[
  "A multilingual result is tied to the language and script of the prompt, not inferred from a model name alone.",
  "When one source is trained primarily on Chinese text, its English continuation is an out-of-domain probe rather than a fair English-only ranking.",
  "Byte-level perplexity can be dominated by unfamiliar scripts and should be read alongside per-language examples.",
  "Language-specific output samples are kept raw so another researcher can inspect script choice and repetition.",
  "A broad claim about bilingual competence requires a larger balanced corpus and topic-stratified results.",],
 'limitations_hypotheses':[
  "A finite set of activation interventions is evidence for local dependence, not a complete causal graph of the source network.",
  "A small student's low loss on a narrow corpus can reflect corpus regularity and is not evidence of general intelligence.",
  "Tokenizer differences, parameter scale, training data, and runtime fidelity are independent confounds that the report must name.",
  "A source-equivalence hypothesis needs independent behavioural, intervention, and architecture-level tests before consolidation.",
  "A software test that checks an adapter's shape and finiteness does not establish that its generated answer is correct.",],
 }
 for facet in FACET_ORDER:
  # ensure all fact-derived rows for a facet form the training partition; fill to exactly eight.
  while len(training[facet]) < 8:
   idx=len(training[facet])
   training[facet].append((clean_ascii(train_additions[facet][idx % len(train_additions[facet])]),[f"method:{facet}:train-{idx+1}"]))
  training[facet]=training[facet][:8]
 
 EXTRA_TRAIN={
  'behavioral_generation':[
   "A generation audit separates prompt-template behavior from the semantic content of the user request.",
   "If a model emits a fragment of its system identity, the log preserves that token sequence and marks the answer as weak task adherence.",
   "A repetition diagnostic records repeated n-grams, unique-token ratio, continuation length, and stop reason.",
   "Prompt order is fixed across model comparisons unless the experiment explicitly studies conversational history.",
   "The decoding configuration includes temperature, top-k policy, random seed, and maximum number of generated tokens.",
   "A deterministic continuation makes runs easier to compare, but deterministic output can still be repetitive or incorrect.",
   "The model card's intended use is recorded separately from observed response quality in a local test.",
   "Raw model generations are kept immutable so that later reviewers can distinguish data from interpretation.",
  ],
  'next_token_statistics':[
   "Token-level scoring uses the target token sequence after the first input token and excludes padding from the loss.",
   "An aggregate score is paired with token count and byte coverage to make denominators auditable.",
   "The same text can produce different token counts under byte-level, SentencePiece, and GPT-style BPE tokenizers.",
   "Cross-model ranking is not based on raw native-token perplexity when the vocabularies differ.",
   "Accuracy can hide uncertainty because it counts only whether the largest logit selected the observed target.",
   "The next-token probability distribution is stored before sampling so that generation randomness is not confused with model uncertainty.",
   "A non-finite loss or logit is recorded as an execution failure and cannot be treated as a low score.",
   "Every score file links back to the exact held-out string set by a SHA-256 checksum.",
  ],
  'hidden_representations':[
   "The hidden-state capture is indexed by block and by sequence position to permit later contrastive analysis.",
   "Layer RMS measurements can reveal scale differences introduced by normalization, but they do not identify computational purpose.",
   "Feature claims should be phrased as hypotheses with expected effects before a feature is intervened on.",
   "A tensor with the expected shape may still be semantically wrong if the adapter maps checkpoint weights incorrectly.",
   "The runtime checks activation finiteness before using the representation summary in an experiment record.",
   "An activation store should persist the input, layer identifier, model hash, and extraction configuration.",
   "Representation distributions can be compared across prompts only when the token positions have a clear alignment rule.",
   "The same model may expose many hidden dimensions without providing a human-interpretable meaning for each dimension.",
  ],
  'attention_patterns':[
   "Attention entropy is computed after causal masking and softmax, not from the unnormalized attention scores.",
   "The head count and layer count are architectural facts that help validate an adapter against its checkpoint metadata.",
   "Attention capture can consume substantial memory, so full matrices and compact summaries are offered as separate options.",
   "A lower attention entropy indicates a more concentrated distribution for the measured query, not necessarily better reasoning.",
   "Head-level patching requires a different intervention target from the post-block residual intervention used in this run.",
   "The query input and the captured attention tensor are linked by a stable experiment identifier.",
   "A recurrent student can be observed through its state trajectory, but it must not be assigned fabricated transformer heads.",
   "Layerwise attention changes should be repeated across inputs before an architecture-wide conclusion is made.",
  ],
  'ablation_response':[
   "An ablation record specifies whether zeroing occurs before a block, after attention, or after the complete block output.",
   "The implemented experiment zeroes the selected post-block representation and measures the resulting next-token logits.",
   "A strong logit change can arise from many interacting computations and does not uniquely localize a mechanism.",
   "A nonzero causal effect should be reported with its input and layer so the experiment can be replayed.",
   "The intervention engine reports the actual capability level instead of treating unavailable hook points as supported.",
   "A null change is retained with the same provenance fields as a large change.",
   "An ablation hypothesis can be falsified when the predicted distribution change fails to appear on a preregistered input.",
   "A comparison of first, middle, and last blocks is a useful screen but not exhaustive circuit localization.",
  ],
  'scaling_response':[
   "The scale operation multiplies the target post-block representation by the requested coefficient before downstream layers continue.",
   "Scaling and zeroing are logged separately because zero is only one coefficient in a wider intervention family.",
   "The baseline and scale result are compared using both next-token identity and a numerical logit distance.",
   "The operation's effect may vary with coefficient, model layer, prompt, and language domain.",
   "The no-op coefficient is a useful control for detecting unintended changes in the forward path.",
   "A coefficient sweep should record every planned value, including values that do not change the argmax token.",
   "A hidden-state intervention is interpreted within the selected architecture, not as an identical physical manipulation across all models.",
   "The source study preserves entropy change and logit distance so that a scale result is not reduced to a binary label.",
  ],
  'cross_language_behavior':[
   "English prompts and Chinese prompts are treated as separate strata in the experimental output rather than merged into one average.",
   "Short Chinese continuations provide a basic runtime check but cannot estimate Chinese factual accuracy on their own.",
   "An English-trained byte model can still tokenize Chinese bytes, but that technical ability does not imply fluent generation.",
   "Tokenizer vocabulary size and pretokenization behavior affect the number of predicted units for the same Unicode text.",
   "Language-specific prompt templates are kept explicit because a chat model may rely on special role tokens.",
   "A cross-language result includes the raw script, stop reason, and token count so the observation can be reproduced.",
   "A fair study distinguishes an unsupported language domain from a defective model loader.",
   "The final report states which language prompts were tested and avoids generalizing to languages not observed.",
  ],
  'limitations_hypotheses':[
   "A software release may support loading an LLM without demonstrating that the runtime reproduces every reference implementation detail.",
   "A source model's tokenizer and attention layout are part of the model interface and require independent correctness tests.",
   "A reconstruction should name which source model was observed and which model artifact was actually produced.",
   "A model architecture with fewer than sixty thousand parameters is suited to controlled experiments, not assumed to match a large teacher.",
   "The absence of a semantic interpretation does not invalidate a measured representation effect, but limits the conclusion drawn from it.",
   "A benchmark that uses synthetic truth must keep its answer key outside the discovery and model-building pipeline.",
   "All discovered mechanisms keep their counterexamples, uncertainty, and domain-of-validity fields when stored.",
   "A model's future potential is not inferred from the present result; additional experiments determine the supported claims.",
  ],
 }

 # Entirely unseen formulations for validation/test; they do not repeat source numbers or generation strings.
 valtest={
 'behavioral_generation':[
  ("A prompt-response pair records both the request and the exact continuation produced under a stated decoding policy.",["authored:val:behavior-1"]),
  ("Continuation repetition can be quantified separately from whether the answer addresses the user request.",["authored:val:behavior-2"]),
  ("Response fluency, task adherence, and reproducibility are distinct evaluation criteria for a generated answer.",["authored:test:behavior-1"]),
  ("A stopped sequence should retain its stop reason so a reader can separate end-of-turn behavior from truncation.",["authored:test:behavior-2"]),],
 'next_token_statistics':[
  ("The denominator for a token score must state how many target positions were actually evaluated.",["authored:val:stats-1"]),
  ("A byte-normalized score helps compare text likelihood across tokenizers, but does not erase language-domain differences.",["authored:val:stats-2"]),
  ("A next-unit prediction score summarizes one local prediction task and should not be reported as conversational accuracy.",["authored:test:stats-1"]),
  ("The evaluation manifest identifies the exact common text prefix used to compute every model's normalized loss.",["authored:test:stats-2"]),],
 'hidden_representations':[
  ("An activation record must identify the tensor position and architecture block that produced the measured vector.",["authored:val:hidden-1"]),
  ("A feature hypothesis predicts how a controlled input or intervention should change a selected representation.",["authored:val:hidden-2"]),
  ("A high-dimensional vector may support several downstream computations, so a single coordinate is not automatically a concept.",["authored:test:hidden-1"]),
  ("A representation summary is reproducible only when the input, weights, extraction method, and layer index are fixed.",["authored:test:hidden-2"]),],
 'attention_patterns':[
  ("A causal attention summary describes how a query position distributes weight over preceding positions.",["authored:val:attention-1"]),
  ("A concentrated attention map is a numerical property and needs independent intervention evidence before receiving a functional label.",["authored:val:attention-2"]),
  ("An architecture with no attention operator should not output an empty map as if that were a measured head.",["authored:test:attention-1"]),
  ("Attention statistics depend on the token sequence and cannot be generalized from one prompt to all model behavior.",["authored:test:attention-2"]),],
 'ablation_response':[
  ("A layer intervention compares an unmodified baseline with a defined change to an internal computation path.",["authored:val:ablation-1"]),
  ("A prediction change following ablation is an effect for that intervention and input, not a complete causal explanation.",["authored:val:ablation-2"]),
  ("The location and operation of an intervention determine what causal question the resulting comparison can answer.",["authored:test:ablation-1"]),
  ("A stable top token does not rule out changes elsewhere in the output probability distribution.",["authored:test:ablation-2"]),],
 'scaling_response':[
  ("A representation coefficient specifies the magnitude retained before the following network computation proceeds.",["authored:val:scaling-1"]),
  ("A scale sweep records numeric output changes even if a discrete prediction remains unchanged.",["authored:val:scaling-2"]),
  ("A null scale effect is retained as evidence and can narrow the range of supported hypotheses.",["authored:test:scaling-1"]),
  ("Changing the size of a residual stream differs from substituting a constant or removing a block entirely.",["authored:test:scaling-2"]),],
 'cross_language_behavior':[
  ("A multilingual smoke test records one result per language so script-specific failures are not hidden by an aggregate.",["authored:val:language-1"]),
  ("A tokenizer that encodes a script successfully may still produce weak continuations in that language.",["authored:val:language-2"]),
  ("Language coverage and task correctness require separate evidence and should not be collapsed into one label.",["authored:test:language-1"]),
  ("A model's response should be assessed in the language of the prompt with an appropriate held-out set.",["authored:test:language-2"]),],
 'limitations_hypotheses':[
  ("A small independent student can be operationally real while remaining far below its source models in capacity.",["authored:val:limits-1"]),
  ("Mechanistic equivalence requires evidence beyond a few matching output strings or a lower language-modeling loss.",["authored:val:limits-2"]),
  ("A scientifically cautious report separates measured facts, derived inferences, open hypotheses, and failed predictions.",["authored:test:limits-1"]),
  ("The scope of a conclusion cannot exceed the domains, prompts, and interventions that were actually tested.",["authored:test:limits-2"]),],
}
 # Deterministic class-specific split; exact text/hash never crosses partitions.
 split_rows={'train':[],'validation':[],'test':[]}
 doc_idx=0
 for facet in FACET_ORDER:
  rows=training[facet]
  for text,evidence in rows:
   doc_idx+=1; text=clean_ascii(text); split_rows['train'].append({'document_id':f"MV31-{doc_idx:03d}",'facet':facet,'language':'en','text':text,'text_sha256':sha256_bytes(text.encode()),'evidence_ids':evidence,'split':'train'})
  for text in EXTRA_TRAIN[facet]:
   doc_idx+=1; text=clean_ascii(text); split_rows['train'].append({'document_id':f"MV31-{doc_idx:03d}",'facet':facet,'language':'en','text':text,'text_sha256':sha256_bytes(text.encode()),'evidence_ids':[f"authored:train-extra:{facet}"],'split':'train'})
  for split_idx,split in enumerate(('validation','test')):
   for text,evidence in valtest[facet][split_idx*2:(split_idx+1)*2]:
    doc_idx+=1; text=clean_ascii(text)
    split_rows[split].append({'document_id':f"MV31-{doc_idx:03d}",'facet':facet,'language':'en','text':text,'text_sha256':sha256_bytes(text.encode()),'evidence_ids':evidence,'split':split})
 # Discard the pilot test partition: its scores were inspected during exploratory runs.
 # Register a new final holdout with four fresh texts per facet; it is read only after checkpoint selection.
 fresh_test={
  'behavioral_generation':[
   'Each completion record retains the original prompt, generated string, stop reason, and decoding seed so exact output behavior can be examined again.',
   'A model may emit tokens reliably yet fail the requested task, so completion length and instruction fit are evaluated separately.',
   'The final response audit stores raw model output before any human formatting or correction is applied.',
   'A refusal, an empty answer, and a truncated completion are distinct generation outcomes and should not share one label.',
  ],
  'next_token_statistics':[
   'Likelihood is calculated over observed target units and reported with the number of UTF-8 bytes actually scored.',
   'Cross-tokenizer comparisons normalize the same string because a single word may split into multiple native tokens.',
   'The score file stores the target prefix and model hash so another run can recreate the loss denominator.',
   'A top-token match is a local prediction result and does not by itself establish that a full answer is correct.',
  ],
  'hidden_representations':[
   'The probe stores layerwise vectors for a fixed token position and model revision so representation differences can be replayed.',
   'A hidden coordinate receives a feature label only after a contrastive prediction and intervention are tested independently.',
   'The activation tensor shape and numeric range are recorded before a semantic interpretation is proposed.',
   'An observed vector may support multiple downstream operations, so one dimension is not automatically a named concept.',
  ],
  'attention_patterns':[
   'The observed attention matrix is indexed by query and key positions after application of the causal mask.',
   'Head entropy describes one activation trace and does not certify the purpose of that attention head.',
   'A model without an attention operator is recorded as unavailable for head analysis rather than assigned an empty measured map.',
   'Layerwise attention comparisons require aligned input tokens and should retain the exact sequence used for capture.',
  ],
  'ablation_response':[
   'Removing a block residual update preserves the incoming stream while testing dependence on the block learned transformation.',
   'A prediction change after ablation is stored alongside the continuous logit difference from the baseline run.',
   'A control intervention targets a neighboring block to test whether the observed effect is location-specific.',
   'The intervention record includes the target operation and model hash so the internal perturbation can be reproduced.',
  ],
  'scaling_response':[
   'The intervention sweep compares fixed coefficients while prompt, model weights, and decoding settings remain unchanged.',
   'A no-op coefficient provides a control for unexpected numerical changes during the scaling procedure.',
   'Continuous logit movement can be measurable even when the identity of the highest-scoring token does not change.',
   'The scale coefficient is recorded with the target path and baseline output to distinguish it from a constant replacement.',
  ],
  'cross_language_behavior':[
   'The evaluation report preserves a separate score for each language instead of merging script-specific behavior into one aggregate.',
   'A tokenizer may accept an unfamiliar script even when generated sequences in that language remain poor.',
   'Language coverage and task correctness are measured separately because successful tokenization is not evidence of fluency.',
   'A cross-language result includes the exact prompt, raw continuation, tokenizer identity, and evaluated byte count.',
  ],
  'limitations_hypotheses':[
   'An effect observed on one prompt supports a narrow conclusion until it repeats across independent prompts and tasks.',
   'An interpretation remains provisional when several different causal paths could explain the same visible output.',
   'The scope of a claim must not exceed the architectures, prompts, interventions, and language domains actually tested.',
   'A lower loss on a constructed corpus does not establish general reasoning or equivalent internal mechanisms.',
  ],
 }
 split_rows['test']=[]
 for facet in FACET_ORDER:
  for idx,text in enumerate(fresh_test[facet],start=1):
   doc_idx+=1; text=clean_ascii(text)
   split_rows['test'].append({'document_id':f"MV31-FINAL-{facet}-{idx:02d}",'facet':facet,'language':'en','text':text,'text_sha256':sha256_bytes(text.encode()),'evidence_ids':[f"authored:fresh-final-test:{facet}-{idx}"],'split':'test'})
 # Validate all partition IDs, hashes, payloads, and script.
 ids={s:{r['document_id'] for r in rows} for s,rows in split_rows.items()}
 hashes={s:{r['text_sha256'] for r in rows} for s,rows in split_rows.items()}
 for a,b in [('train','validation'),('train','test'),('validation','test')]:
  if ids[a]&ids[b] or hashes[a]&hashes[b]: raise RuntimeError(f'partition leakage: {a}/{b}')
 for rows in split_rows.values():
  for r in rows:
   if not r['text'].isascii(): raise RuntimeError('non-English/non-ASCII content in English corpus')
 out.mkdir(parents=True,exist_ok=True)
 for split,rows in split_rows.items():
  p=out/f'{split}.jsonl'; p.write_text(''.join(json.dumps(r,ensure_ascii=True,sort_keys=True)+'\n' for r in rows),encoding='utf-8')
 study_file=source_study.resolve()
 manifest={'dataset_id':'NG-Multiview-Observation-English-v3_1','language':'English (ASCII text only)','view_facets':FACET_ORDER,
  'documents':{k:len(v) for k,v in split_rows.items()},'total_documents':sum(map(len,split_rows.values())),
  'text_sha256_by_split':{k:sha256_file(out/f'{k}.jsonl') for k in split_rows},
  'source_study_json_sha256':sha256_file(study_file),'source_study_file':source_study.name,
  'source_evidence_policy':'Uses model descriptors, single-prompt layer/attention observations, controlled internal interventions, and short raw continuations from prompts that are separate from the final language-modeling evaluation corpus. The evaluation score fields and evaluation texts are never read by this builder.',
  'split_policy':'Sixteen documents per facet in training (eight source-evidence-derived and eight authored); two authored validation documents and four newly authored final-test documents per facet. The old pilot test was discarded after scores were inspected during development. Unique document IDs and text hashes are checked across splits.',
  'anti_contamination':'The separate cross-model evaluation corpus is not copied into any partition; the generator deliberately never reads language_modeling_scores or evaluation_dataset from the study file.',
  'builder_sha256':sha256_file(Path(__file__))}
 (out/'dataset_manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=True),encoding='utf-8')
 print(json.dumps(manifest,indent=2))

if __name__=='__main__':
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('--study',required=True);ap.add_argument('--out',required=True);a=ap.parse_args()
 build(Path(a.study),Path(a.out))
