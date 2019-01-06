<!-- : --- Self-Elevating Batch Script ---------------------------
@whoami /groups | find "S-1-16-12288" > nul && goto :admin
set "ELEVATE_CMDLINE=cd /d "%~dp0" & call "%~f0" %*"
cscript //nologo "%~f0?.wsf" //job:Elevate & exit /b

-->
<job id="Elevate"><script language="VBScript">
  Set objShell = CreateObject("Shell.Application")
  Set objWshShell = WScript.CreateObject("WScript.Shell")
  Set objWshProcessEnv = objWshShell.Environment("PROCESS")
  strCommandLine = Trim(objWshProcessEnv("ELEVATE_CMDLINE"))
  objShell.ShellExecute "cmd", "/c " & strCommandLine, "", "runas"
</script></job>
:admin -----------------------------------------------------------

@echo off
echo Running as elevated user.
echo Script file : %~f0
echo Arguments   : %*
echo Working dir : %cd%
echo.
:: administrator commands here
:: e.g., run shell as admin


:: StartService work begins here.
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
	call %_STARTSERVICE_PROC% Pipeline_Loadout %_INPUT_FILE%
)  ELSE echo ~ Workspace could not be found

ENDLOCAL

:: Restore original directory
POPD

:: pause