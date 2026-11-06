@echo off
setlocal EnableExtensions DisableDelayedExpansion
cd /d "%~dp0" || exit /b 1

rem Prefer the project virtual environment; otherwise use the installed Python launcher.
if exist ".venv\Scripts\python.exe" (
  set "PYTHON=.venv\Scripts\python.exe"
  goto check_python
)
where py >nul 2>nul
if not errorlevel 1 (
  set "PYTHON=py -3"
  goto check_python
)
where python >nul 2>nul
if not errorlevel 1 (
  set "PYTHON=python"
  goto check_python
)
goto no_python

:check_python
%PYTHON% -c "import sys; print(sys.version); assert sys.version_info >= (3,11), 'Python 3.11 or newer is required'"
if errorlevel 1 goto bad_python
set "PYTHONPATH=%CD%\src;%PYTHONPATH%"
set "NGEGB_V3_1_HOME=%CD%\workspace"

if /I "%~1"=="install" goto install
if /I "%~1"=="bootstrap" goto install
if /I "%~1"=="install-hf" goto install_hf
if /I "%~1"=="status" goto status
if /I "%~1"=="test" goto test
if /I "%~1"=="web" goto web
if /I "%~1"=="examples" goto examples
if /I "%~1"=="report" goto report
if /I "%~1"=="doctor" goto doctor
if "%~1"=="" goto help
%PYTHON% ngbrain.py %*
exit /b %errorlevel%

:install
if not exist ".venv\Scripts\python.exe" (
  echo [NGeGenBrain] Creating project virtual environment...
  %PYTHON% -m venv .venv
  if errorlevel 1 goto install_failed
)
if not exist ".venv\Scripts\python.exe" goto install_failed
.venv\Scripts\python.exe -m pip install --upgrade pip
if errorlevel 1 goto install_failed
.venv\Scripts\python.exe -m pip install -e ".[torch,analysis]" sentencepiece safetensors pytest
if errorlevel 1 goto install_failed
echo [OK] Dependencies installed into .venv.
echo Optional generic Hugging Face loader: ngbrain_NGeGenBrain_v3_1.bat install-hf
exit /b 0

:install_hf
if not exist ".venv\Scripts\python.exe" (
  echo Run ngbrain_NGeGenBrain_v3_1.bat install first.
  exit /b 2
)
.venv\Scripts\python.exe -m pip install -e ".[huggingface]"
exit /b %errorlevel%

:status
%PYTHON% ngbrain.py status
exit /b %errorlevel%

:test
%PYTHON% -m compileall -q src ngbrain.py scripts tests
if errorlevel 1 exit /b 1
%PYTHON% -m pytest -q
exit /b %errorlevel%

:web
%PYTHON% scripts\launch_web.py --host 127.0.0.1 --port 8767
exit /b %errorlevel%

:examples
%PYTHON% ngbrain.py benchmark --bits 4 --seed 20261028 --max-samples 4096
if errorlevel 1 exit /b 1
%PYTHON% ngbrain.py synthetic-ladder --seed 20261028
exit /b %errorlevel%

:report
%PYTHON% ngbrain.py report --output "%CD%\audit\rapport_latest_NGeGenBrain_v3_1.md"
exit /b %errorlevel%

:doctor
%PYTHON% -c "import sys,torch,numpy,sentencepiece; print('Python:',sys.version); print('PyTorch:',torch.__version__); print('NumPy:',numpy.__version__); print('SentencePiece:',sentencepiece.__version__)"
if errorlevel 1 exit /b 1
%PYTHON% ngbrain.py status
exit /b %errorlevel%

:help
echo NGeGenBrain v3_1 launcher
echo Usage: ngbrain_NGeGenBrain_v3_1.bat COMMAND [arguments]
echo   install / bootstrap  create .venv and install core dependencies
echo   install-hf          install optional generic Hugging Face adapter
echo   status              show version, environment and registry integrity
echo   test                compile and execute the full pytest suite
echo   web                 start local server and open the browser after health check
echo   examples            run reproducible synthetic benchmark examples
echo   doctor              check runtime dependencies and workspace
echo   model local --paths PATH --load PATH  discover/load local models
echo   chat --model-path PATH --prompt TEXT  run local model generation
echo   report              write the current CLI report
exit /b 0

:no_python
echo [ERROR] Python 3.11 or newer is required. Install Python from python.org, then retry.
exit /b 2
:bad_python
echo [ERROR] The selected Python is too old or failed its environment check.
exit /b 2
:install_failed
echo [ERROR] Bootstrap failed. Check network access, disk space and the Python installation.
exit /b 1
