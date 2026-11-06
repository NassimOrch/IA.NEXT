from order59.audit import StaticAuditor
from pathlib import Path

def test_static_audit_clean():
    r=StaticAuditor().scan(Path(__file__).parents[1]/'src')
    assert r['pass']


def test_general_core_has_no_evaluation_adapter_imports():
    src=(Path(__file__).parents[1]/"src/order59").rglob("*.py")
    text="\n".join(p.read_text(errors="replace") for p in src)
    assert "evaluation_adapters" not in text
    assert "ChessEnv" not in text
    assert "HiddenPermutationEnv" not in text


def test_core_excludes_evaluation_adapters_by_layout():
    root=Path(__file__).parents[1]
    assert not (root/'src/order59/environments.py').exists()
    assert not (root/'src/order59/cli.py').exists()
    assert (root/'evaluation_adapters/environments.py').exists()


def test_static_audit_rejects_forbidden_imports(tmp_path):
    p=tmp_path/'bad.py'; p.write_text('import socket\n')
    r=StaticAuditor().scan(tmp_path)
    assert not r['pass'] and r['forbidden_imports']
