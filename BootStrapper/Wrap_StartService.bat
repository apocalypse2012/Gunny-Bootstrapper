@echo off

:: Store current directory and change to environment directory so script works in any path.
%~d0
cd %~dp0
PUSHD %~dp0

CALL "D:\Program Files (x86)\Python27\python" %cd%\WrapToExe.py Gunny.py

rem // Restore original directory
POPD