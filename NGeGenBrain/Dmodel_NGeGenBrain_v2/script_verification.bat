@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (echo Python launcher 'py' required.& exit /b 2)
set "PYTHONPATH=%CD%\src"
py -3.11 -m compileall -q src ngbrain.py
if errorlevel 1 exit /b 1
py -3.11 -m unittest discover -s tests -v
if errorlevel 1 exit /b 1
set "VERIFY_WS=%TEMP%\NGeGenBrain_v2_verification_workspace"
py -3.11 ngbrain.py --workspace "%VERIFY_WS%" benchmark --bits 4 --seed 20261027 --max-samples 4096
if errorlevel 1 exit /b 1
py -3.11 scripts\verify_archive_manifest.py --root "%CD%"
if errorlevel 1 exit /b 1
set "VERIFY_OUT=%TEMP%\NGeGenBrain_v2_validation"
py -3.11 scripts\validate_release.py --output-dir "%VERIFY_OUT%"
exit /b %errorlevel%
