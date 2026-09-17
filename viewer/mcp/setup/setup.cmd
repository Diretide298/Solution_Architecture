@echo off
rem Double-click this to create your project folder and connect Claude Code to ADAM.
rem It runs setup.ps1 - in adam-connector\ beside this file in the zip, or beside
rem it in the installed copy - past the "running scripts is disabled" policy for
rem this one run only. Nothing about the computer's policy is changed.
set "ADAM_SETUP=%~dp0adam-connector\setup.ps1"
if exist "%~dp0setup.ps1" set "ADAM_SETUP=%~dp0setup.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File "%ADAM_SETUP%" %*
set RESULT=%ERRORLEVEL%
rem Kept open when double-clicked, so the result can be read. Not when run with
rem arguments from a terminal, where the window is already yours.
if "%~1"=="" pause
exit /b %RESULT%
