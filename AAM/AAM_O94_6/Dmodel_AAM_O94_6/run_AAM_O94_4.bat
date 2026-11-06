@echo off
setlocal EnableExtensions
rem AAM O94.4 standalone Windows launcher with persistent diagnostics.
cd /d "%~dp0"
if not exist "%~dp0logs\O94_4" mkdir "%~dp0logs\O94_4" >nul 2>nul
set "AAM_LOG=%~dp0logs\O94_4\launcher_windows.log"
set "AAM_EXIT=1"
echo ============================================================ > "%AAM_LOG%" 2>&1
echo AAM O94.4 Windows startup - %DATE% %TIME% >> "%AAM_LOG%" 2>&1
echo Package root: %CD% >> "%AAM_LOG%" 2>&1
echo ============================================================ >> "%AAM_LOG%" 2>&1

where py.exe >nul 2>nul
if not errorlevel 1 goto use_py
where python.exe >nul 2>nul
if errorlevel 1 goto no_python
set "AAM_PYTHON=python"
goto check_python

:use_py
set "AAM_PYTHON=py -3"

:check_python
echo Interpreter command: %AAM_PYTHON% >> "%AAM_LOG%" 2>&1
%AAM_PYTHON% -c "import sys; print('Python:',sys.version); raise SystemExit(0 if sys.version_info >= (3,11) else 1)" >> "%AAM_LOG%" 2>&1
if errorlevel 1 goto old_python
%AAM_PYTHON% -c "import tkinter; print('Tkinter: OK')" >> "%AAM_LOG%" 2>&1
if errorlevel 1 goto no_tk
set "PYTHONPATH=%~dp0;%PYTHONPATH%"

rem Run the exact preflight explicitly and persist its diagnostic before starting Tk.
%AAM_PYTHON% -c "import json; from pathlib import Path; from aam_o93.preflight import preflight; r=preflight(Path.cwd(), 'launcher:windows'); print(json.dumps(r,ensure_ascii=False)); raise SystemExit(0 if r.get('status') == 'PASS_BOUNDED' else 20)" >> "%AAM_LOG%" 2>&1
if errorlevel 1 goto preflight_failed

echo Starting AAM O94.4 desktop UI... >> "%AAM_LOG%" 2>&1
%AAM_PYTHON% -m aam_o93 ui >> "%AAM_LOG%" 2>&1
set "AAM_EXIT=%ERRORLEVEL%"
if not "%AAM_EXIT%"=="0" goto launch_failed
echo AAM closed normally. Exit code 0. >> "%AAM_LOG%" 2>&1
exit /b 0

:no_python
set "AAM_EXIT=9009"
echo ERROR: Python 3.11+ was not found. Install Python with Tcl/Tk support. >> "%AAM_LOG%" 2>&1
goto fail

:old_python
set "AAM_EXIT=2"
echo ERROR: AAM O94.4 requires Python 3.11 or newer. >> "%AAM_LOG%" 2>&1
goto fail

:no_tk
set "AAM_EXIT=3"
echo ERROR: Tkinter/Tcl is unavailable in the selected Python. Repair this Python installation or install Python with Tcl/Tk. >> "%AAM_LOG%" 2>&1
goto fail

:preflight_failed
set "AAM_EXIT=20"
echo ERROR: startup preflight blocked. See the JSON diagnostic above. >> "%AAM_LOG%" 2>&1
goto fail

:launch_failed
if "%AAM_EXIT%"=="0" set "AAM_EXIT=1"
echo ERROR: AAM O94.4 exited with code %AAM_EXIT%. >> "%AAM_LOG%" 2>&1
goto fail

:fail
echo.
echo AAM O94.4 could not start. Diagnostic log:
echo "%AAM_LOG%"
echo.
if exist "%AAM_LOG%" type "%AAM_LOG%"
echo.
echo Correct the reported prerequisite or send this log with the bug report.
pause
exit /b %AAM_EXIT%
