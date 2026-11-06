from __future__ import annotations
from pathlib import Path
import ast, re
class StaticAuditor:
    VERSION="O59_STATIC_AUDITOR_2"
    def scan(self,root):
        issues=[]; dispatch=[]; imports=[]
        for p in Path(root).rglob("*.py"):
            text=p.read_text(errors="replace")
            try: tree=ast.parse(text)
            except SyntaxError as e:
                issues.append({"file":str(p),"issue":"syntax", "detail":str(e)}); continue
            for node in ast.walk(tree):
                if isinstance(node,ast.Call):
                    if isinstance(node.func,ast.Name) and node.func.id in {"eval","exec"}: issues.append({"file":str(p),"issue":node.func.id})
                    if isinstance(node.func,ast.Attribute) and isinstance(node.func.value,ast.Name) and node.func.value.id=="os" and node.func.attr=="system": issues.append({"file":str(p),"issue":"os.system"})
                if isinstance(node,ast.Compare) and isinstance(node.left,ast.Name) and node.left.id in {"benchmark","task","family","task_name"}: dispatch.append({"file":str(p),"line":getattr(node,"lineno",0)})
                if isinstance(node,(ast.Import,ast.ImportFrom)):
                    names=[a.name for a in getattr(node,"names",[])]
                    if any(n.split('.')[0] in {"socket","requests","urllib","subprocess","ctypes"} for n in names):
                        imports.append({"file":str(p),"line":getattr(node,"lineno",0),"names":names})
            if re.search(r"(?:solutions?|answers?)\s*=\s*\{", text, re.I):
                issues.append({"file":str(p),"issue":"solution-table-pattern"})
        return {"forbidden_calls":issues,"forbidden_imports":imports,"benchmark_dispatch_candidates":dispatch,"pass":not issues and not imports and not dispatch}

