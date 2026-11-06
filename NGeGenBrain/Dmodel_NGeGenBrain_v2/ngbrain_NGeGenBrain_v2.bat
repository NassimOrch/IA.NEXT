@echo off
setlocal EnableExtensions
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 goto no_python
py -3.11 -c "import sys; assert sys.version_info >= (3,11); print(sys.version)"
if errorlevel 1 goto bad_python
set "PYTHON=py -3.11"
if exist ".venv\Scripts\python.exe" set "PYTHON=.venv\Scripts\python.exe"
set "PYTHONPATH=%CD%\src"
if /I "%~1"=="install" goto install
if /I "%~1"=="bootstrap" goto install
if /I "%~1"=="status" goto status
if /I "%~1"=="test" goto test
if /I "%~1"=="web" goto web
if /I "%~1"=="examples" goto examples
if /I "%~1"=="report" goto report
if "%~1"=="" goto help
%PYTHON% ngbrain.py %*
exit /b %errorlevel%

:install
if not exist ".venv\Scripts\python.exe" (
  py -3.11 -m venv .venv
  if errorlevel 1 exit /b 1
)
.venv\Scripts\python.exe -m pip install --upgrade pip
if errorlevel 1 exit /b 1
.venv\Scripts\python.exe -m pip install -e ".[torch]"
if errorlevel 1 (
  echo Installation failed. Check network access and consult README.md for manual dependency setup.
  exit /b 1
)
echo Bootstrap completed. Use: ngbrain_NGeGenBrain_v2.bat status
echo For local Hugging Face model support: .venv\Scripts\python.exe -m pip install -e ".[huggingface]"
exit /b 0

:status
%PYTHON% ngbrain.py status
exit /b %errorlevel%

:test
%PYTHON% -m compileall -q src ngbrain.py scripts tests
if errorlevel 1 exit /b 1
%PYTHON% -m unittest discover -s tests -v
if errorlevel 1 exit /b 1
set "PYTHONPATH=%CD%\legacy_NGeGenBrain_v1\src"
%PYTHON% -m unittest discover -s legacy_NGeGenBrain_v1\tests -v
exit /b %errorlevel%

:web
%PYTHON% ngbrain.py serve --host 127.0.0.1 --port 8766
exit /b %errorlevel%

:examples
%PYTHON% ngbrain.py benchmark --bits 4 --seed 20261027 --max-samples 4096
if errorlevel 1 exit /b 1
%PYTHON% ngbrain.py synthetic-ladder --seed 20261027
if errorlevel 1 exit /b 1
%PYTHON% ngbrain.py compose --file examples\compose_xor.json
exit /b %errorlevel%

:report
%PYTHON% ngbrain.py report --output "%TEMP%\latest_NGeGenBrain_v2.md"
exit /b %errorlevel%

:help
echo NGeGenBrain_v2 command launcher
echo Usage: ngbrain_NGeGenBrain_v2.bat COMMAND [ngbrain arguments]
echo   install/bootstrap  create .venv and install PyTorch support
echo   status             show workspace status
echo   test               compile and run V2 and preserved V1 tests
echo   web                launch loopback Web UI
echo   examples           run synthetic reconstruction and ladder examples
echo   report             write a local report
echo   [CLI command]      invoke ngbrain.py directly
exit /b 0

:no_python
echo Python 3.11+ launcher 'py' is required. Install Python from python.org.
exit /b 2
:bad_python
echo Python 3.11 or newer is required.
exit /b 2
