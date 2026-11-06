@echo off
setlocal EnableExtensions DisableDelayedExpansion
cd /d "%~dp0" || exit /b 1
if not exist "%~dp0ngbrain_NGeGenBrain_v3_1.bat" (
  echo [ERROR] Missing ngbrain_NGeGenBrain_v3_1.bat beside this launcher.
  pause
  exit /b 2
)
if not exist "%~dp0.venv\Scripts\python.exe" (
  echo [NGeGenBrain] First launch: installing local dependencies into .venv.
  call "%~dp0ngbrain_NGeGenBrain_v3_1.bat" install
  if errorlevel 1 goto failed
)
call "%~dp0ngbrain_NGeGenBrain_v3_1.bat" web
set "RC=%ERRORLEVEL%"
if not "%RC%"=="0" goto failed_with_code
exit /b 0

:failed
echo [ERROR] Setup failed. Read the message above; the application was not started.
pause
exit /b 1
:failed_with_code
echo [ERROR] NGeGenBrain did not start or stopped with exit code %RC%.
echo Run ngbrain_NGeGenBrain_v3_1.bat doctor and ngbrain_NGeGenBrain_v3_1.bat test for diagnostics.
pause
exit /b %RC%
