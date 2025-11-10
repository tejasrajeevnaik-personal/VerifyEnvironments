@echo off
echo Important: This file should always reside in project root. If needed copy its shortcut to a desired location.

REM Config
set PYTHON_EXE=python.exe

REM Execute tests
%PYTHON_EXE% -m pytest
%PYTHON_EXE% -m utilities.send_report

pause
