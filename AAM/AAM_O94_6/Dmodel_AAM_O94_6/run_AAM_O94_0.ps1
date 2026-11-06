$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$python = $null
$pythonArgs = @()
if (Get-Command py.exe -ErrorAction SilentlyContinue) { $python = 'py.exe'; $pythonArgs = @('-3') }
elseif (Get-Command python.exe -ErrorAction SilentlyContinue) { $python = 'python.exe' }
else { Write-Error 'Python 3.11+ introuvable. Installer Python avec Tcl/Tk.'; exit 9009 }
& $python @pythonArgs -c 'import sys; raise SystemExit(0 if sys.version_info >= (3,11) else 1)'
if ($LASTEXITCODE -ne 0) { Write-Error 'AAM O94_0 exige Python 3.11 ou plus récent.'; exit 2 }
& $python @pythonArgs -c 'import tkinter'
if ($LASTEXITCODE -ne 0) { Write-Error 'Tkinter indisponible. Réparer Python avec Tcl/Tk.'; exit 3 }
$env:PYTHONPATH = "$PSScriptRoot;$env:PYTHONPATH"
& $python @pythonArgs -m aam_o93 ui
exit $LASTEXITCODE
