@echo off

set _LINK_PATH=%cd%
set _SCRIPT_PATH=%~dp0
set _INPUT_FILE=%1

:: Store current directory and change to environment directory so script works in any path.
%~d0
cd %~dp0
PUSHD %~dp0

:: Keep changes local
SETLOCAL enableDelayedExpansion

echo ~ Creating Workspace Pipeline folders

set _STARTSERVICE_PROC=StartService.exe

IF EXIST !_STARTSERVICE_PROC! (
	call %_STARTSERVICE_PROC% Pipeline_Loadout %_INPUT_FILE% --copy
)  ELSE echo ~ Maxplay Workspace could not be found

ENDLOCAL

:: Restore original directory
POPD

:: pause