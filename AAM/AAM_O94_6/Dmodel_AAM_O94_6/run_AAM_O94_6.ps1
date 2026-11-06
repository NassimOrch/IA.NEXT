$ErrorActionPreference = "Stop"
Set-Location -LiteralPath $PSScriptRoot
python scripts/preflight_o946.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m aam_o93 ui
exit $LASTEXITCODE
