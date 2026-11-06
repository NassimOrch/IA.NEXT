@echo off
setlocal
cd /d "%~dp0"
if not exist checksums.sha256 exit /b 2
where certutil >nul 2>nul || exit /b 3
for %%F in (Dmodel_NGeGenBrain_v3.zip Amodel_NGeGenBrain_v3.zip suivi_model_NGeGenBrain_v3.zip model_produit_NG_v3.zip) do (
  if not exist "%%F" exit /b 4
)
echo Archives present. Use certutil -hashfile FILE SHA256 to compare against checksums.sha256.
exit /b 0
