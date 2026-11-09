@echo off
setlocal
REM Extract both independent ZIP parts into one folder and verify every SHA-256.
REM Usage: reassemble_suivi_model_eSond_v2.bat [part1.zip] [part2.zip] [destination]
set "PART1=%~1"
set "PART2=%~2"
set "DEST=%~3"
if "%PART1%"=="" set "PART1=%CD%\suivi_model_eSond_v2.zip"
if "%PART2%"=="" set "PART2=%CD%\suivi_model_eSond_v2_part2.zip"
if "%DEST%"=="" set "DEST=%CD%\suivi_model_eSond_v2_extracted"
if not exist "%PART1%" (echo Missing ZIP part 1: %PART1% & exit /b 2)
if not exist "%PART2%" (echo Missing ZIP part 2: %PART2% & exit /b 2)
if not exist "%DEST%" mkdir "%DEST%"
powershell -NoProfile -ExecutionPolicy Bypass -Command "Expand-Archive -LiteralPath '%PART1%' -DestinationPath '%DEST%' -Force; Expand-Archive -LiteralPath '%PART2%' -DestinationPath '%DEST%' -Force"
if errorlevel 1 exit /b %errorlevel%
python "%DEST%\suivi_model_eSond_v2\scripts\verify_suivi_package.py" "%DEST%\suivi_model_eSond_v2"
if errorlevel 1 exit /b %errorlevel%
echo Verified package extracted at: %DEST%\suivi_model_eSond_v2
endlocal
