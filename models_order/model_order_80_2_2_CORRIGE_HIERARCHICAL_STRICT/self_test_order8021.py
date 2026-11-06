#!/usr/bin/env python3
from __future__ import annotations
import json, tempfile
from pathlib import Path
from src.order80.general_engine import GeneralResearchEngine
from src.order80.budget import parse_duration
from src.order80.reference_catalog import ReferenceCatalog
from src.order80.security import validate_url

def main():
    assert parse_duration('1h') == 3600.0 and parse_duration('1week') == 604800.0
    for bad in ('file:///tmp/x','ftp://example.org/x','https://user:pass@example.org/x','https://127.0.0.1/x'):
        try: validate_url(bad,{'example.org'},set())
        except ValueError: pass
        else: raise AssertionError(f'unsafe URL accepted: {bad}')
    with tempfile.TemporaryDirectory(prefix='order8021-selftest-') as td:
        root=Path(td); docs=root/'docs'; docs.mkdir()
        (docs/'a.md').write_text('Allowlist trusted destinations.\n\nDisable unsafe redirects.\n\nApply timeouts to web requests.',encoding='utf-8')
        task=root/'task.json'; refs=root/'refs.json'; out=root/'out'
        task.write_text(json.dumps({'title':'generic control test','problem':'Explain safe web reference controls.','objective':'Give an evidence-backed answer.','required_terms':['allowlist','redirects','timeouts'],'verification':{'mode':'provenance_coverage','min_unique_sources':1}},ensure_ascii=False),encoding='utf-8')
        refs.write_text(json.dumps({'local':[str(docs)],'web':{'enabled':False},'engine':{'duration':'2s','local_batch':2,'rag_batch':2}},ensure_ascii=False),encoding='utf-8')
        result=GeneralResearchEngine(task,refs,out,out/'memory.json',{'duration':'2s','idle_sleep_seconds':0.05}).run()
        assert result['resolution_status']=='EVIDENCE_SYNTHESIS_VERIFIED', result
        assert list((out/'news').glob('*/demonstration.txt'))
        assert (out/'checkpoint.json').exists() and (out/'events.jsonl').exists()
    print('ORDER80.2.1 SELF-TEST PASS')
if __name__=='__main__': raise SystemExit(main())
