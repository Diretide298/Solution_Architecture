@echo off
rem Double-click this to remove the ADAM connector from Claude Code.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup.ps1" -Uninstall %*
set RESULT=%ERRORLEVEL%
if "%~1"=="" pause
exit /b %RESULT%
