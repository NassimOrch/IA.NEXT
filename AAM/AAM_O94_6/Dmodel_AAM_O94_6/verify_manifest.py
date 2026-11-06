from __future__ import annotations
import hashlib,json,sys
from pathlib import Path
IGNORED_DIRS={"__pycache__",".pytest_cache",".git"}
def sha(p:Path)->str:
 h=hashlib.sha256()
 with p.open("rb") as f:
  for block in iter(lambda:f.read(1024*1024),b""):h.update(block)
 return h.hexdigest()
def main():
 root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve(); mf=root/'MANIFEST_SHA256.json'
 doc=json.loads(mf.read_text(encoding='utf-8')); bad=[]
 excluded=set(doc.get('excluded_manifest_files',[]))
 expected=set()
 for row in doc['files']:
  rel=row['path']; expected.add(rel); p=root/rel
  if not p.is_file(): bad.append({'path':rel,'error':'MISSING'}); continue
  size=p.stat().st_size; h=sha(p)
  if size!=row['size_bytes'] or h!=row['sha256']: bad.append({'path':rel,'error':'HASH_OR_SIZE_MISMATCH','actual_sha256':h,'actual_size':size})
 actual=set()
 for p in root.rglob('*'):
  rel=p.relative_to(root)
  if not p.is_file() or p.name in excluded or rel.as_posix().startswith('sav_AAM_O94_6/current/') or any(part in IGNORED_DIRS for part in rel.parts) or p.suffix in {'.pyc','.pyo','.lock','.tmp'} or p.name.endswith('.tmp'): continue
  actual.add(rel.as_posix())
 extra=sorted(actual-expected); omitted=sorted(expected-actual)
 for x in extra: bad.append({'path':x,'error':'UNMANIFESTED_EXTRA_FILE'})
 print(json.dumps({'status':'PASS' if not bad else 'FAIL','checked':len(expected),'extra_count':len(extra),'missing_or_changed_count':sum(1 for x in bad if x['error']!='UNMANIFESTED_EXTRA_FILE'),'bad':bad},indent=2))
 return 0 if not bad else 2
if __name__=='__main__': raise SystemExit(main())
