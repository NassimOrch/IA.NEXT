@echo off
setlocal
cd /d "%~dp0"
if "%~1"=="" (echo Usage: script_reassemblage.bat Dmodel_NGeGenBrain_v2.zip& exit /b 2)
where py >nul 2>nul
if errorlevel 1 (echo Python launcher required.& exit /b 2)
py -3.11 scripts\reassemble_bundle.py "%~1"
exit /b %errorlevel%
