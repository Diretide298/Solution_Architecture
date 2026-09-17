@echo off
rem Double-click this to connect Claude Code to ADAM.
rem It runs setup.ps1 beside it, past the "running scripts is disabled" policy
rem for this one run only - nothing about the computer's policy is changed.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup.ps1" %*
set RESULT=%ERRORLEVEL%
rem Kept open when double-clicked, so the result can be read. Not when run with
rem arguments from a terminal, where the window is already yours.
if "%~1"=="" pause
exit /b %RESULT%
