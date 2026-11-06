@echo off
setlocal
call "%~dp0tools\select_python_windows.bat"
if errorlevel 1 exit /b %errorlevel%
start "NGeGenBrain_v0 local server" "%~dp0run_web_NGeGenBrain_v0.bat"
set "READY=0"
for /L %%I in (1,1,20) do (
  powershell -NoProfile -Command "try { $r = Invoke-WebRequest -UseBasicParsing -Uri 'http://127.0.0.1:8765/' -TimeoutSec 1; if ($r.StatusCode -eq 200) { exit 0 } else { exit 1 } } catch { exit 1 }" >nul 2>&1
  if not errorlevel 1 (set "READY=1" & goto open_browser)
  timeout /t 1 /nobreak >nul
)
echo NGeGenBrain_v0 did not become ready at http://127.0.0.1:8765/.
echo Check that the port is free and inspect the server window for errors.
exit /b 1
:open_browser
start "" "http://127.0.0.1:8765/"
exit /b 0
