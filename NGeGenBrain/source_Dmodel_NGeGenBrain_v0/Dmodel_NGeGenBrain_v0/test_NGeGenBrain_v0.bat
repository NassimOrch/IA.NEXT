@echo off
setlocal
cd /d "%~dp0"
set "NGEGB_HOME=%LOCALAPPDATA%\NGeGenBrain_v0"
call "%~dp0tools\select_python_windows.bat"
if errorlevel 1 exit /b 9009
if "%NGEGB_PY_KIND%"=="launcher" goto run_launcher
if "%NGEGB_PY_KIND%"=="python" goto run_python
 goto run_embedded
:run_launcher
"%NGEGB_PY_CMD%" -3 -W error::ResourceWarning "%~dp0ngbrain.py" test
goto finish
:run_python
"%NGEGB_PY_CMD%" -W error::ResourceWarning "%~dp0ngbrain.py" test
goto finish
:run_embedded
"%NGEGB_PY_CMD%" -W error::ResourceWarning "%~dp0ngbrain.py" test
:finish
set "NGEGB_EXIT=%ERRORLEVEL%"
endlocal & exit /b %NGEGB_EXIT%
