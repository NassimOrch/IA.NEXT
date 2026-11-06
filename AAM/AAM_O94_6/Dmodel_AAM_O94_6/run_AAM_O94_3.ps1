$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$python = $null; $pythonArgs = @()
if (Get-Command py.exe -ErrorAction SilentlyContinue) { $python='py.exe'; $pythonArgs=@('-3') }
elseif (Get-Command python.exe -ErrorAction SilentlyContinue) { $python='python.exe' }
else { Write-Error 'Python 3.11+ introuvable.'; exit 9009 }
$logDir = Join-Path $PSScriptRoot 'logs\O94_3'
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$log = Join-Path $logDir 'launcher_windows_ps1.log'
"AAM O94.3 PowerShell startup - $(Get-Date -Format o)" | Set-Content -Encoding UTF8 $log
"Package root: $PSScriptRoot" | Add-Content -Encoding UTF8 $log
& $python @pythonArgs -c 'import sys; print("Python:",sys.version); raise SystemExit(0 if sys.version_info >= (3,11) else 1)' 2>&1 | Tee-Object -FilePath $log -Append
if ($LASTEXITCODE -ne 0) { Write-Error 'AAM O94.3 exige Python 3.11 ou supérieur.'; Read-Host 'Entrée pour fermer'; exit 2 }
& $python @pythonArgs -c 'import tkinter; print("Tkinter: OK")' 2>&1 | Tee-Object -FilePath $log -Append
if ($LASTEXITCODE -ne 0) { Write-Error 'Tk/Tcl indisponible.'; Read-Host 'Entrée pour fermer'; exit 3 }
$env:PYTHONPATH = "$PSScriptRoot;$env:PYTHONPATH"
"Running O94.3 preflight" | Add-Content -Encoding UTF8 $log
& $python @pythonArgs -c 'import json; from pathlib import Path; from aam_o93.preflight import preflight; r=preflight(Path.cwd(), "launcher:windows-ps1"); print(json.dumps(r, ensure_ascii=False, indent=2)); raise SystemExit(0 if r.get("status") == "PASS_BOUNDED" else 20)' 2>&1 | Tee-Object -FilePath $log -Append
if ($LASTEXITCODE -ne 0) { Write-Error "AAM O94.3 preflight failed. See $log"; Get-Content $log; Read-Host 'Entrée pour fermer'; exit 20 }
"Starting AAM O94.3 desktop UI" | Add-Content -Encoding UTF8 $log
& $python @pythonArgs -m aam_o93 ui 2>&1 | Tee-Object -FilePath $log -Append
$rc=$LASTEXITCODE
if ($rc -ne 0) { Write-Error "AAM O94.3 exited with code $rc. See $log"; Get-Content $log; Read-Host 'Entrée pour fermer' }
exit $rc
