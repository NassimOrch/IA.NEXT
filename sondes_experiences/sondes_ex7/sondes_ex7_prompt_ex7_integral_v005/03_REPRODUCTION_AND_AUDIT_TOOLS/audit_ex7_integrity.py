import json,csv,hashlib,zipfile,sys
from pathlib import Path
import numpy as np
import torch
root=Path('/mnt/data/sondes_research_workspace_ex7/versions/sondes_ex7_v001__2026-10-31')
issues=[]; summary={}
# text JSON files
json_ok=0
for p in root.rglob('*.json'):
    try:
        d=json.loads(p.read_text())
        def no_nan(x):
            if isinstance(x,float): return np.isfinite(x)
            if isinstance(x,dict): return all(no_nan(v) for v in x.values())
            if isinstance(x,list): return all(no_nan(v) for v in x)
            return True
        if not no_nan(d): issues.append(f'nonfinite JSON: {p.relative_to(root)}')
        json_ok+=1
    except Exception as e: issues.append(f'bad JSON {p.relative_to(root)}: {e}')
# CSVs
csv_ok=0
for p in root.rglob('*.csv'):
    try:
        with p.open(newline='') as f:
            rows=list(csv.reader(f))
        if rows and any(len(r)!=len(rows[0]) for r in rows): issues.append(f'CSV ragged: {p.relative_to(root)}')
        csv_ok+=1
    except Exception as e: issues.append(f'bad CSV {p.relative_to(root)}: {e}')
# npy
npy_ok=0
for p in root.rglob('*.npy'):
    try:
        a=np.load(p,allow_pickle=False)
        if a.size and np.issubdtype(a.dtype,np.number) and not np.isfinite(a).all(): issues.append(f'nonfinite NPY: {p.relative_to(root)}')
        npy_ok+=1
    except Exception as e: issues.append(f'bad NPY {p.relative_to(root)}: {e}')
# pt torch serialization
pt_ok=0
for i,p in enumerate(root.rglob('*.pt'),1):
    try:
        x=torch.load(p,map_location='cpu',weights_only=False)
        # scan tensors for finite values, but tolerate optimiser integer tensors
        def scan(obj,path=''):
            if isinstance(obj,torch.Tensor):
                if obj.is_floating_point() or obj.is_complex():
                    if obj.numel() and not torch.isfinite(obj).all(): issues.append(f'nonfinite tensor: {p.relative_to(root)}:{path}')
            elif isinstance(obj,dict):
                for k,v in obj.items(): scan(v,f'{path}/{k}')
            elif isinstance(obj,(list,tuple)):
                for j,v in enumerate(obj): scan(v,f'{path}/{j}')
        scan(x)
        pt_ok+=1
    except Exception as e: issues.append(f'bad PT {p.relative_to(root)}: {type(e).__name__}: {e}')
# npz sources in working data
npzfiles=list(Path('/mnt/data/ex7_working_copy_ex6').rglob('*.npz'))
npz_ok=[]
for p in npzfiles:
    try:
        with np.load(p,allow_pickle=False) as z:
            details={k:{'shape':list(z[k].shape),'dtype':str(z[k].dtype),'finite':bool(np.isfinite(z[k]).all()) if np.issubdtype(z[k].dtype,np.number) else None} for k in z.files}
        npz_ok.append({'file':str(p),'arrays':details})
    except Exception as e: issues.append(f'bad NPZ {p}: {e}')
summary={'json_valid':json_ok,'csv_valid':csv_ok,'npy_valid':npy_ok,'pt_valid':pt_ok,'npz_valid':len(npz_ok),'npz_details':npz_ok,'issues':issues}
Path('/mnt/data/EX7_INTEGRITY_AUDIT.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='npz_details'},indent=2,ensure_ascii=False))
for x in npz_ok: print('NPZ',x)
