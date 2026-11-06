@echo off
setlocal
cd /d "%~dp0"
py -3 scripts\preflight_o946.py
if errorlevel 1 exit /b %errorlevel%
py -3 -m aam_o93 ui
exit /b %errorlevel%
