@echo off
setlocal
cd /d "%~dp0"
set "NGEGB_HOME=%LOCALAPPDATA%\NGeGenBrain_v1"
if not exist "%NGEGB_HOME%\data" mkdir "%NGEGB_HOME%\data"
call "%~dp0tools\select_python_windows.bat"
if errorlevel 1 exit /b 9009
if "%NGEGB_PY_KIND%"=="launcher" goto run_launcher
if "%NGEGB_PY_KIND%"=="python" goto run_python
 goto run_embedded
:run_launcher
"%NGEGB_PY_CMD%" -3 "%~dp0ngbrain.py" serve --host 127.0.0.1 --port 8765
goto finish
:run_python
"%NGEGB_PY_CMD%" "%~dp0ngbrain.py" serve --host 127.0.0.1 --port 8765
goto finish
:run_embedded
"%NGEGB_PY_CMD%" "%~dp0ngbrain.py" serve --host 127.0.0.1 --port 8765
:finish
set "NGEGB_EXIT=%ERRORLEVEL%"
endlocal & exit /b %NGEGB_EXIT%
