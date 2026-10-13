@echo off
rem Double-click this to remove the ADAM connector from Claude Code, and ADAM's
rem usage hooks from your Claude Code settings (only ADAM's - nothing else there).
rem Project folders it created are left exactly as they are.
set "ADAM_SETUP=%~dp0adam-connector\setup.ps1"
if exist "%~dp0setup.ps1" set "ADAM_SETUP=%~dp0setup.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File "%ADAM_SETUP%" -Uninstall %*
set RESULT=%ERRORLEVEL%
if "%~1"=="" pause
exit /b %RESULT%
