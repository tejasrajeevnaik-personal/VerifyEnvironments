@echo off
REM ====== CONFIG ======
set PYTHON_EXE="C:\Program Files\Python314\python.exe"
set TEST_DIR=C:\Users\P7167349\OneDrive - Ness Digital Engineering\3_Personal\PythonLearning\VerifyEnvironments\tests
set REPORT_DIR=C:\Users\P7167349\OneDrive - Ness Digital Engineering\3_Personal\PythonLearning\VerifyEnvironments\reports
set REPORT_FILE=%REPORT_DIR%\report.html

REM ====== RUN TESTS ======
echo Running pytest tests ...

REM Ensure reports folder exists
if not exist "%REPORT_DIR%" mkdir "%REPORT_DIR%"

%PYTHON_EXE% -m pytest "%TEST_DIR%" --html="%REPORT_FILE%"

echo.
echo Tests finished. Report saved to %REPORT_FILE%
pause
