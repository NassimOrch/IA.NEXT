@echo off
setlocal EnableExtensions
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" goto use_venv
where py >nul 2>nul
if errorlevel 1 goto try_python
set "PYTHON=py -3"
goto check_python
:try_python
where python >nul 2>nul
if errorlevel 1 goto no_python
set "PYTHON=python"
goto check_python
:use_venv
set "PYTHON=.venv\Scripts\python.exe"
:check_python
%PYTHON% -c "import sys; assert sys.version_info >= (3,11), 'Python 3.11+ required'; print(sys.version)"
if errorlevel 1 goto bad_python
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
if not exist ".venv\Scripts\python.exe" (py -3.11 -m venv .venv || exit /b 1)
.venv\Scripts\python.exe -m pip install --upgrade pip
if errorlevel 1 exit /b 1
.venv\Scripts\python.exe -m pip install -e ".[torch]"
if errorlevel 1 exit /b 1
echo Bootstrap completed.
exit /b 0
:status
%PYTHON% ngbrain.py status
exit /b %errorlevel%
:test
%PYTHON% -m compileall -q src ngbrain.py scripts tests
if errorlevel 1 exit /b 1
%PYTHON% -m unittest discover -s tests -v
exit /b %errorlevel%
:web
%PYTHON% ngbrain.py serve --host 127.0.0.1 --port 8767
exit /b %errorlevel%
:examples
%PYTHON% ngbrain.py benchmark --bits 4 --seed 20261028 --max-samples 4096
if errorlevel 1 exit /b 1
%PYTHON% ngbrain.py synthetic-ladder --seed 20261028
exit /b %errorlevel%
:report
%PYTHON% ngbrain.py report --output "%CD%\audit\rapport_latest_NGeGenBrain_v3_0.md"
exit /b %errorlevel%
:help
echo NGeGenBrain v3_0 launcher
echo Usage: ngbrain_NGeGenBrain_v3_0.bat COMMAND [arguments]
echo   install/bootstrap  create .venv and install the torch dependencies
echo   status             show version, environment and registry integrity
echo   test               compile and run the full unittest suite
echo   web                launch the local Web UI on 127.0.0.1:8767
echo   examples           run synthetic benchmark examples
echo   produce-multifacet-tinylm  train the official v3_0 English multi-facet tiny LM
echo   model local --paths PATH --load PATH  load a local model
echo   chat --model-path PATH --prompt TEXT  run local generation
exit /b 0
:no_python
echo Python Launcher 'py' with Python 3.11+ is required.
exit /b 2
:bad_python
echo Python 3.11 or newer is required.
exit /b 2
