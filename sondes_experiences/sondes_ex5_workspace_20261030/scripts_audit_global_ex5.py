from pathlib import Path
import json, hashlib, collections, csv, sys, math
import numpy as np
ROOT=Path('/mnt/data/sondes_research_workspace_ex5')
VERS=ROOT/'versions'
OUT=ROOT/'deliverables'
OUT.mkdir(exist_ok=True)
# shared metrics implementation, same function used in experiments
sys.path.insert(0,str(VERS/'sondes_ex5_v001__2026-10-30'/'src'))
from ex5_common import calc_metrics

def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()
def resolve_ref(s, version_root):
    p=Path(s)
    if p.is_absolute(): return p
    # Most runs store paths relative to the owning version.
    p1=version_root/p
    if p1.exists(): return p1
    p2=ROOT/p
    if p2.exists(): return p2
    return p1

report={"workspace":str(ROOT),"prompt_sha256":sha(Path('/mnt/data/prompt_ex5.json')),
        "versions":{},"global":{},"exceptions":[],"issues":[]}
json_total=jsonl_total=jsonl_lines=0
json_parse_errors=[]; jsonl_parse_errors=[]
checkpoint_refs=[]; prediction_refs=[]; stale_legacy=[]
raw_prediction_recalculations=[]; metric_errors=[]
ratio_records=[]; run_counts={}
for vdir in sorted(VERS.iterdir()):
    if not vdir.is_dir(): continue
    ver=vdir.name
    jfiles=list(vdir.rglob('*.json'))
    lfiles=list(vdir.rglob('*.jsonl'))
    jn=ln=0
    for p in jfiles:
        try: json.loads(p.read_text()); jn+=1
        except Exception as e: json_parse_errors.append({"file":str(p.relative_to(ROOT)),"error":str(e)})
    for p in lfiles:
        for no,line in enumerate(p.read_text().splitlines(),1):
            if not line.strip(): continue
            try: json.loads(line); ln+=1
            except Exception as e: jsonl_parse_errors.append({"file":str(p.relative_to(ROOT)),"line":no,"error":str(e)})
    json_total+=jn; jsonl_total+=len(lfiles); jsonl_lines+=ln
    vcp=[]; vpred=[]; vratio=[]; vpred_recalc=[]
    # Walk all registries with file references.
    for p in lfiles:
        rows=[]
        for line in p.read_text().splitlines():
            if line.strip():
                try: rows.append(json.loads(line))
                except: continue
        run_counts[f'{ver}/{p.relative_to(vdir)}']=len(rows)
        for idx,r in enumerate(rows,1):
            cp=r.get('checkpoint')
            if isinstance(cp,dict) and cp.get('path') and cp.get('sha256'):
                f=resolve_ref(cp['path'],vdir); ok=f.is_file() and sha(f)==cp['sha256']
                item={"registry":str(p.relative_to(ROOT)),"row":idx,"path":str(f),"ok":ok}
                checkpoint_refs.append(item); vcp.append(item)
            for c in r.get('checkpoint_files',[]) if isinstance(r.get('checkpoint_files'),list) else []:
                if isinstance(c,dict) and c.get('path') and c.get('sha256'):
                    f=resolve_ref(c['path'],vdir); ok=f.is_file() and sha(f)==c['sha256']
                    item={"registry":str(p.relative_to(ROOT)),"row":idx,"path":str(f),"ok":ok}
                    checkpoint_refs.append(item); vcp.append(item)
            # Candidate/MLP capacity ratios from all registries.
            kind=r.get('comparison_kind')
            if kind=='ge4x' and r.get('ratio_vs_probe') is not None:
                val=float(r['ratio_vs_probe'])
                ratio_records.append({"version":ver,"registry":str(p.relative_to(ROOT)),"candidate":r.get('candidate_id'),"seed":r.get('model_seed'),"ratio":val,"ok":val>=4.0})
            elif 'ratio' in r and ('ge4' in str(r.get('comparison_kind','')).lower() or 'ge4x' in str(r.get('comparison_kind','')).lower()):
                val=float(r['ratio']);ratio_records.append({"version":ver,"registry":str(p.relative_to(ROOT)),"candidate":r.get('candidate_id'),"seed":r.get('model_seed'),"ratio":val,"ok":val>=4.0})
            # Canonical prediction refs. V1 superseded v3 unsuffixed refs are documented and superseded by corrected per-seed files.
            pf=r.get('prediction_file'); ph=r.get('prediction_sha256')
            if pf and ph:
                is_old_v3 = (ver.endswith('v001__2026-10-30') and p.name in {
                    'external_v3_wine_probe_runs.jsonl','external_v3_digits_probe_runs.jsonl',
                    'external_v3_wine_probe_runs_corrected.jsonl','external_v3_digits_probe_runs_corrected.jsonl'})
                if is_old_v3:
                    stale_legacy.append({"registry":str(p.relative_to(ROOT)),"row":idx,"seed":r.get('model_seed'),"candidate":r.get('candidate_id'),"path":pf,"reason":"non-unique legacy filename; corrected per-seed sidecar is canonical"})
                else:
                    f=resolve_ref(pf,vdir); ok=f.is_file() and sha(f)==ph
                    item={"registry":str(p.relative_to(ROOT)),"row":idx,"path":str(f),"ok":ok}
                    prediction_refs.append(item);vpred.append(item)
            cpf=r.get('prediction_file_corrected'); cph=r.get('prediction_sha256_corrected')
            if cpf and cph:
                f=resolve_ref(cpf,vdir);ok=f.is_file() and sha(f)==cph
                item={"registry":str(p.relative_to(ROOT)),"row":idx,"path":str(f),"ok":ok,"corrected":True}
                prediction_refs.append(item);vpred.append(item)
    # Recompute each raw prediction JSON with y_true/probabilities.
    for p in (vdir/'results'/'raw').glob('*.json'):
        try: d=json.loads(p.read_text())
        except: continue
        if isinstance(d,dict) and 'y_true' in d and 'probabilities' in d:
            try:
                m=calc_metrics(d['y_true'],d['probabilities'])
                stored=d.get('metrics',{})
                diffs={k:{"stored":float(val),"recomputed":float(m[k])} for k,val in stored.items() if isinstance(val,(int,float)) and k in m and abs(float(val)-float(m[k]))>5e-6}
                item={"file":str(p.relative_to(ROOT)),"metrics_compared":len(stored),"divergences":diffs,"ok":not diffs}
                raw_prediction_recalculations.append(item);vpred_recalc.append(item)
                if diffs: metric_errors.append(item)
            except Exception as e:
                item={"file":str(p.relative_to(ROOT)),"error":str(e),"ok":False}
                raw_prediction_recalculations.append(item);vpred_recalc.append(item);metric_errors.append(item)
    # Dataset-specific test outputs, where available.
    vreport={"json_files_valid":jn,"jsonl_files":len(lfiles),"jsonl_lines_valid":ln,
             "checkpoint_refs":len(vcp),"checkpoint_hash_failures":sum(not x['ok'] for x in vcp),
             "canonical_prediction_refs":len(vpred),"prediction_hash_failures":sum(not x['ok'] for x in vpred),
             "raw_prediction_json_recalculated":len(vpred_recalc),"metric_recalculation_errors":sum(not x['ok'] for x in vpred_recalc)}
    report['versions'][ver]=vreport

ratio_bad=[r for r in ratio_records if not r['ok']]
cp_bad=[r for r in checkpoint_refs if not r['ok']]
pred_bad=[r for r in prediction_refs if not r['ok']]
report['global']={
 "json_files_valid":json_total,"json_parse_errors":len(json_parse_errors),
 "jsonl_files":jsonl_total,"jsonl_valid_lines":jsonl_lines,"jsonl_parse_errors":len(jsonl_parse_errors),
 "checkpoint_hash_refs":len(checkpoint_refs),"checkpoint_hash_failures":len(cp_bad),
 "canonical_prediction_hash_refs":len(prediction_refs),"canonical_prediction_hash_failures":len(pred_bad),
 "legacy_superseded_prediction_pointers":len(stale_legacy),
 "raw_prediction_json_files_recalculated":len(raw_prediction_recalculations),"metric_recalculation_errors":len(metric_errors),
 "MLP_ge4x_ratio_rows":len(ratio_records),"MLP_ge4x_below_4":len(ratio_bad),
 "minimum_MLP_to_probe_ratio":min([x['ratio'] for x in ratio_records],default=None),
 "unique_run_registries":len(run_counts)
}
report['exceptions']=[
 {"id":"V1_EXTERNAL_V3_LEGACY_PATHS","count":len(stale_legacy),"handling":"legacy shared filenames were overwritten across seeds in initial append-only registries; corrected per-seed sidecars are canonical and hash verified; original registries untouched"},
 {"id":"V1_RETRO_DUPLICATE","count":1,"handling":"retro_linear seed 1501 repeated registry row; checkpoint/prediction equal but train time conflicts; both preserved, one canonical row used for compute-resource summaries"},
 {"id":"V1_V4_METADATA_FLAG","count":1,"handling":"supervised joint two-level raw row has overbroad Q_ONLY_UNSUPERVISED flag; training graph verified supervised; correction table supplied, raw row preserved"},
 {"id":"V007_HISTORICAL_EX4","count":1,"handling":"historic EX4 global registry has 95 rows while an old test expected 70; separate filtered audits used"},
 {"id":"V1_REUSE_MLP_CACHES","count":1,"handling":"v004/v005 link records reuse exact MLP cache by parameter count and seed; not counted as newly trained unique MLPs"}
]
report['issues']={"json_parse":json_parse_errors[:100],"jsonl_parse":jsonl_parse_errors[:100],"checkpoint_hash":cp_bad[:100],"prediction_hash":pred_bad[:100],"metric_recalc":metric_errors[:100],"ratio_below4":ratio_bad[:100]}
report['overall_data_integrity_pass']=(not json_parse_errors and not jsonl_parse_errors and not cp_bad and not pred_bad and not metric_errors and not ratio_bad)
# Write report and row-level audit files.
(OUT/'audit_integrite_global_ex5.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
with open(OUT/'audit_ratios_mlp_ge4x_global.csv','w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['version','registry','candidate','seed','ratio','ok']);w.writeheader();w.writerows(ratio_records)
with open(OUT/'audit_predictions_hashes_global.csv','w',newline='') as f:
 rows=prediction_refs+[{**x,'ok':False,'legacy_superseded':True} for x in stale_legacy]
 w=csv.DictWriter(f,fieldnames=sorted(set().union(*(r.keys() for r in rows))) if rows else ['ok']);w.writeheader();w.writerows(rows)
with open(OUT/'audit_checkpoint_hashes_global.csv','w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['registry','row','path','ok']);w.writeheader();w.writerows(checkpoint_refs)
with open(OUT/'audit_metric_recalculation_global.csv','w',newline='') as f:
 rows=[{k:(json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v) for k,v in x.items()} for x in raw_prediction_recalculations]
 w=csv.DictWriter(f,fieldnames=['file','metrics_compared','divergences','error','ok']);w.writeheader();w.writerows(rows)
with open(OUT/'audit_run_registry_counts.csv','w',newline='') as f:
 w=csv.writer(f);w.writerow(['registry','rows']);w.writerows(sorted(run_counts.items()))
print(json.dumps(report['global']|{"overall_data_integrity_pass":report['overall_data_integrity_pass'],"by_version":report['versions']},indent=2,ensure_ascii=False))
if not report['overall_data_integrity_pass']: raise SystemExit(1)
