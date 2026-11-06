@echo off
setlocal EnableExtensions
rem Compatibility launcher for the current O94.1 delivery; all diagnostics are handled by the canonical launcher.
echo This launcher name is retained for compatibility. Starting AAM O94.1.
call "%~dp0run_AAM_O94_1.bat"
exit /b %ERRORLEVEL%
