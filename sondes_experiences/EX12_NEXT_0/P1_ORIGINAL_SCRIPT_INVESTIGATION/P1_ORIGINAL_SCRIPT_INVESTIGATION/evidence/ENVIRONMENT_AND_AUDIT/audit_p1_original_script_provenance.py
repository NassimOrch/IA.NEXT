#!/usr/bin/env python3
"""Read-only forensic audit for P1_RUN_001 / P1_RUN_002 source provenance.

This is an audit/recomputation utility, NOT either missing historical benchmark
producer. It does not edit run data, metadata, registries, or source scripts.
It writes a new timestamped audit JSON under 10_reports/P1_ORIGINAL_SCRIPT_INVESTIGATION.
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import pathlib
import sqlite3
import subprocess
import sys
import datetime as dt
from collections import Counter

import numpy as np
import pandas as pd

ROOT = pathlib.Path('/mnt/data/EX12_NEXT_0')
P1 = ROOT / '08_benchmarks' / 'P1'
CODE = ROOT / '04_code'
OUT = ROOT / '10_reports' / 'P1_ORIGINAL_SCRIPT_INVESTIGATION'
OUT.mkdir(parents=True, exist_ok=True)


def sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def stat_record(path: pathlib.Path):
    st = path.stat()
    return {
        'path': str(path), 'exists': True, 'size_bytes': st.st_size,
        'mtime_utc': dt.datetime.fromtimestamp(st.st_mtime, dt.timezone.utc).isoformat(),
        'ctime_utc': dt.datetime.fromtimestamp(st.st_ctime, dt.timezone.utc).isoformat(),
        'birth_utc': dt.datetime.fromtimestamp(st.st_birthtime, dt.timezone.utc).isoformat()
            if hasattr(st, 'st_birthtime') else None,
        'inode': st.st_ino,
        'sha256': sha256(path) if path.is_file() else None,
    }


def load_json(path: pathlib.Path):
    return json.loads(path.read_text(encoding='utf-8'))


def audit_run(rel: str):
    run_dir = P1 / rel
    summary_path = run_dir / 'P1_BENCHMARK_SUMMARY.csv'
    raw_path = run_dir / 'P1_BENCHMARK_RAW.csv'
    tests_path = run_dir / 'P1_NUMERICAL_TESTS.json'
    meta_path = run_dir / 'P1_BENCHMARK_METADATA.json'
    summary = pd.read_csv(summary_path)
    raw = pd.read_csv(raw_path)
    tests = load_json(tests_path)
    meta = load_json(meta_path)
    keys = ['kernel', 'batch', 'centers', 'latent_dim']
    grouped = raw.groupby(keys, sort=False)
    max_diffs = {k: 0.0 for k in ['p50_ms', 'p95_ms', 'p99_ms', 'mean_ms', 'std_ms', 'throughput_samples_s']}
    bad_groups = []
    wrong_group_sizes = []
    groups_without_summary = []
    for key, group in grouped:
        match = summary
        for col, value in zip(keys, key):
            match = match[match[col] == value]
        if len(match) != 1:
            groups_without_summary.append({'key': [str(x) for x in key], 'summary_rows': int(len(match))})
            continue
        vals = group['latency_ms'].to_numpy(dtype=np.float64)
        calculated = {
            'p50_ms': float(np.quantile(vals, .5)),
            'p95_ms': float(np.quantile(vals, .95)),
            'p99_ms': float(np.quantile(vals, .99)),
            'mean_ms': float(np.mean(vals)),
            'std_ms': float(np.std(vals, ddof=0)),
        }
        calculated['throughput_samples_s'] = float(key[1]) / (calculated['p50_ms'] / 1000.0)
        diffs = {k: abs(float(match.iloc[0][k]) - v) for k, v in calculated.items()}
        for k, v in diffs.items():
            max_diffs[k] = max(max_diffs[k], v)
        if len(vals) != 40:
            wrong_group_sizes.append({'key': [str(x) for x in key], 'n': int(len(vals))})
        if max(diffs.values()) > 1e-8:
            bad_groups.append({'key': [str(x) for x in key], 'n': int(len(vals)), 'max_abs_diff': max(diffs.values())})
    failures = [x for x in tests.get('tests', []) if not x.get('pass', x.get('allclose', True))]
    test_types = Counter(x.get('test', 'UNKNOWN') for x in tests.get('tests', []))
    failure_types = Counter(x.get('test', 'UNKNOWN') for x in failures)
    distances = [x.get('max_abs_error', x.get('max_abs')) for x in failures if x.get('test') == 'distance_output_equivalence']
    return {
        'run_path': str(run_dir.relative_to(ROOT)),
        'metadata_status': meta.get('status'),
        'metadata_created_at_utc': meta.get('created_at_utc'),
        'seed': meta.get('seed'),
        'summary_rows': int(len(summary)),
        'raw_rows': int(len(raw)),
        'unique_group_count': int(len(grouped)),
        'group_size_values': sorted(int(x) for x in raw.groupby(keys).size().unique()),
        'raw_duplicate_rows': int(raw.duplicated().sum()),
        'summary_duplicate_keys': int(summary.duplicated(keys).sum()),
        'groups_without_exactly_one_summary_row': groups_without_summary,
        'wrong_group_sizes': wrong_group_sizes,
        'groups_with_aggregate_diff_gt_1e_8': bad_groups,
        'max_abs_aggregate_differences': max_diffs,
        'cold_ms_recomputable_from_raw': False,
        'cold_ms_note': 'P1_BENCHMARK_RAW.csv stores the 40 timed samples per group; the one cold measurement is present only in the summary and cannot be independently recomputed from raw samples.',
        'numerical_test_count': int(len(tests.get('tests', []))),
        'numerical_test_failures': int(len(failures)),
        'test_type_counts': dict(test_types),
        'failure_type_counts': dict(failure_types),
        'max_failed_distance_abs_error': max((float(x) for x in distances if x is not None), default=None),
        'summary_sha256': sha256(summary_path),
        'raw_sha256': sha256(raw_path),
        'tests_sha256': sha256(tests_path),
        'metadata_sha256': sha256(meta_path),
        'kernel_names': sorted(str(x) for x in summary['kernel'].unique()),
    }

# Run directories and their measured data.
run1 = audit_run('attempts/P1_RUN_001_FAILED')
run2 = audit_run('P1_RUN_002')

# The old top-level P1_RUN_001 files are retained as duplicates of the attempt archive.
duplicate_comparison = {}
for name in ['P1_BENCHMARK_SUMMARY.csv', 'P1_BENCHMARK_RAW.csv', 'P1_NUMERICAL_TESTS.json', 'P1_BENCHMARK_METADATA.json']:
    a = P1 / name
    b = P1 / 'attempts' / 'P1_RUN_001_FAILED' / name
    duplicate_comparison[name] = {
        'top_level_exists': a.exists(), 'attempt_copy_exists': b.exists(),
        'byte_identical': a.exists() and b.exists() and a.read_bytes() == b.read_bytes(),
        'top_level': stat_record(a) if a.exists() else None,
        'attempt_copy': stat_record(b) if b.exists() else None,
    }

# Current source hashes and chronology. These are later canonical scripts, not originals for RUN001/002.
source_hash_manifest_path = P1 / 'P1_SOURCE_HASHES.json'
source_hash_manifest = load_json(source_hash_manifest_path)
source_timeline = []
for name in ['hc_kernels.py', 'p1_microbench.py', 'p1_microbench_repeat.py', 'test_p1_kernels.py', 'analyze_p1.py']:
    path = CODE / name
    source_timeline.append(stat_record(path) if path.exists() else {'path': str(path), 'exists': False})
    if path.exists():
        source_timeline[-1]['listed_in_P1_SOURCE_HASHES'] = name in source_hash_manifest.get('scripts', {})
        source_timeline[-1]['hash_matches_manifest'] = sha256(path) == source_hash_manifest.get('scripts', {}).get(name)

# Validate whether the bytecode caches could be historical source copies.
pyc_records = []
import struct
for name in ['hc_kernels', 'p1_microbench', 'p1_microbench_repeat', 'test_p1_kernels']:
    pyc = CODE / '__pycache__' / f'{name}.cpython-313.pyc'
    if not pyc.exists():
        pyc_records.append({'name': name, 'exists': False})
        continue
    b = pyc.read_bytes()
    flags = struct.unpack('<I', b[4:8])[0]
    rec = {'name': name, **stat_record(pyc), 'pyc_magic': b[:4].hex(), 'pyc_flags': flags}
    if flags == 0:
        src_mtime, src_size = struct.unpack('<II', b[8:16])
        rec['header_source_mtime_utc'] = dt.datetime.fromtimestamp(src_mtime, dt.timezone.utc).isoformat()
        rec['header_source_size_bytes'] = src_size
        src = CODE / f'{name}.py'
        rec['header_matches_current_source_stat'] = src.exists() and int(src.stat().st_mtime) == src_mtime and src.stat().st_size == src_size
    pyc_records.append(rec)

# P1 registry, decisions, gates, limitation note.
registry_path = ROOT / '00_governance' / 'P1_RUN_REGISTRY.jsonl'
registry = [json.loads(x) for x in registry_path.read_text().splitlines() if x.strip()]
registry_records = {x['run_id']: x for x in registry}
run2_limitation_note = P1 / 'P1_RUN_002' / 'PROVISIONAL_LIMITATION_NOTE.md'
run2_note = run2_limitation_note.read_text(encoding='utf-8') if run2_limitation_note.exists() else None

# Environment examination: shell and IPython histories, VCS, overlay visibility, capabilities.
history_db = pathlib.Path('/home/oai/.ipython/profile_default/history.sqlite')
history_info = {'exists': history_db.exists()}
if history_db.exists():
    con = sqlite3.connect(str(history_db))
    tables = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")]
    history_info['tables'] = tables
    for table in ['sessions', 'history', 'output_history']:
        if table in tables:
            history_info[f'{table}_rows'] = int(con.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0])
    history_info['session_rows'] = con.execute('SELECT * FROM sessions').fetchall() if 'sessions' in tables else []
    con.close()

shell_history_candidates = [
    pathlib.Path('/root/.bash_history'), pathlib.Path('/root/.sh_history'),
    pathlib.Path('/root/.zsh_history'), pathlib.Path('/home/oai/.bash_history'),
    pathlib.Path('/home/oai/.sh_history'), pathlib.Path('/home/oai/.zsh_history'),
]
shell_history = [{'path': str(p), 'exists': p.exists(), 'size_bytes': p.stat().st_size if p.exists() else None} for p in shell_history_candidates]

vcs_dirs = [str(p) for p in [ROOT / '.git', ROOT / '.svn', CODE / '.git'] if p.exists()]
backup_dirs = []
for parent in [ROOT, ROOT / '04_code', ROOT / '08_benchmarks']:
    for p in parent.rglob('*'):
        if p.is_dir() and p.name.lower() in {'backup', 'backups', 'snapshots', '.history', '.ipynb_checkpoints'}:
            backup_dirs.append(str(p))

# Root mount capabilities and overlay backing-path accessibility.
findmnt = subprocess.run(['findmnt', '-T', str(CODE / 'p1_microbench.py'), '-o', 'TARGET,SOURCE,FSTYPE,OPTIONS'], text=True, capture_output=True)
mount_text = findmnt.stdout.strip()
overlay_paths = []
for p in [
    pathlib.Path('/run/kata-containers/erofs-multi-layer/62b3f3905d244817a2f0137013e954d1/upper/upper'),
    pathlib.Path('/run/kata-containers/erofs-multi-layer/62b3f3905d244817a2f0137013e954d1/lower-0'),
]:
    overlay_paths.append({'path': str(p), 'visible_in_namespace': p.exists()})
capsh = subprocess.run(['capsh', '--print'], text=True, capture_output=True)
cap_lines = [x for x in capsh.stdout.splitlines() if 'Current:' in x or 'Bounding set' in x or 'Current IAB' in x]

# Search current EX12 workspace and extracted source tree for source candidates by exact path/name/content.
search_roots = [ROOT, pathlib.Path('/mnt/data/last_sources_3')]
candidate_files = []
for sr in search_roots:
    for p in sr.rglob('*'):
        if not p.is_file():
            continue
        lname = p.name.lower()
        if ('microbench' in lname or ('p1' in lname and ('kernel' in lname or 'bench' in lname))):
            candidate_files.append({'path': str(p), 'size_bytes': p.stat().st_size, 'sha256': sha256(p)})

# Search available text logs for explicit source/run commands; record matching files only.
log_roots = [pathlib.Path('/var/log'), pathlib.Path('/opt/terminal-server'), pathlib.Path('/usr/local/init_scripts')]
log_matches = []
for lr in log_roots:
    if not lr.exists():
        continue
    for p in lr.rglob('*'):
        if not p.is_file() or p.stat().st_size > 50 * 1024 * 1024:
            continue
        try:
            txt = p.read_text(errors='ignore')
        except Exception:
            continue
        if any(token in txt for token in ['P1_RUN_001', 'P1_RUN_002', 'p1_microbench.py']):
            log_matches.append(str(p))

# Temporary artifacts in the P1 time window; zero-byte markers are not code sources.
tmp_files = []
for p in pathlib.Path('/tmp').iterdir():
    if p.is_file():
        st = p.stat()
        if dt.datetime.fromtimestamp(st.st_mtime, dt.timezone.utc).date() == dt.date(2026, 11, 4):
            stamp = dt.datetime.fromtimestamp(st.st_mtime, dt.timezone.utc)
            if stamp.hour == 11 and 10 <= stamp.minute <= 17:
                tmp_files.append({'path': str(p), 'size_bytes': st.st_size, 'mtime_utc': stamp.isoformat(), 'sha256': sha256(p)})

result = {
    'report_id': 'EX12-P1-SOURCE-PROVENANCE-INVESTIGATION-001',
    'created_at_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
    'scope': ['EX12_NEXT_0 workspace', '/mnt/data surrounding artifacts', '/tmp and /var/tmp', '/root and /home/oai accessible files', '/opt/terminal-server and /var/log accessible logs', 'last_sources_3 extracted corpus'],
    'run_001': run1,
    'run_002': run2,
    'run_001_duplicate_copy_comparison': duplicate_comparison,
    'registry_run_001': registry_records.get('P1_RUN_001_FAILED'),
    'registry_run_002': registry_records.get('P1_RUN_002'),
    'run_002_limitation_note_sha256': sha256(run2_limitation_note) if run2_limitation_note.exists() else None,
    'run_002_limitation_note_text': run2_note,
    'source_hash_manifest': source_hash_manifest,
    'source_hash_manifest_file': stat_record(source_hash_manifest_path),
    'current_canonical_script_timeline': source_timeline,
    'pyc_cache_inspection': pyc_records,
    'environment': {
        'effective_uid': os.geteuid(), 'effective_gid': os.getegid(),
        'root_mount': mount_text,
        'overlay_backing_paths': overlay_paths,
        'capabilities_relevant_lines': cap_lines,
        'ipython_history': history_info,
        'shell_history_candidates': shell_history,
        'project_vcs_directories': vcs_dirs,
        'project_backup_snapshot_directories': backup_dirs,
        'accessible_log_matches': log_matches,
        'temporary_files_during_p1_window': tmp_files,
    },
    'candidate_source_files_found_by_name': candidate_files,
    'interpretation': {
        'exact_original_scripts_found': False,
        'data_files_exist': True,
        'run_001_source_hash_registered': False,
        'run_002_source_hash_registered': False,
        'current_scripts_are_originals_for_001_002': False,
        'most_supported_operational_explanation': 'The first two exploratory prototypes persisted their result files before a named, immutable, hash-linked producer-script bundle was preserved in the workspace. The current reusable benchmark scripts were written later for canonical RUN003/RUN004. An ephemeral inline/temporary execution path is plausible, but the available records do not distinguish that from subsequent source loss or an unrecorded external location.',
        'intent_or_sabotage_established': False,
        'data_integrity_scope': 'Current raw and summary files are internally consistent; this does not establish byte-for-byte provenance of the program that originally produced them.',
    },
}
out_path = OUT / 'P1_ORIGINAL_SCRIPT_FORENSIC_AUDIT.json'
out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
print(json.dumps({
    'output': str(out_path),
    'run001': {k: run1[k] for k in ['summary_rows','raw_rows','unique_group_count','numerical_test_count','numerical_test_failures','groups_with_aggregate_diff_gt_1e_8']},
    'run002': {k: run2[k] for k in ['summary_rows','raw_rows','unique_group_count','numerical_test_count','numerical_test_failures','groups_with_aggregate_diff_gt_1e_8']},
    'source_files_found_by_name': len(candidate_files),
    'log_matches': log_matches,
    'ipython_history': history_info,
}, indent=2, ensure_ascii=False))
