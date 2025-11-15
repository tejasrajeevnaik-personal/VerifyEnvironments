@echo off
echo Important: This file should always reside in project root. If needed, copy its shortcut to a desired location.
echo.

REM -- Config
set "PYTHON_EXE=C:\Program Files\Python314\python.exe"

REM -- Execute tests (use call so control returns)
call "%PYTHON_EXE%" -m pytest
set "rc=%ERRORLEVEL%"

REM -- Only send report for exit codes 0 and 1
if "%rc%"=="0" (
    call "%PYTHON_EXE%" -m utilities.report
) else if "%rc%"=="1" (
    call "%PYTHON_EXE%" -m utilities.report
) else (
    echo Test execution exited unexpectedly with exit code %rc%. Report sending cancelled.
)

echo.
echo Press any key to close this window . . .
pause >nul
exit /b %rc%
