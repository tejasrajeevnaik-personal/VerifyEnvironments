# Important: This file should always reside in project root. If needed, copy its shortcut to a desired location

Write-Host "Important: This file should always reside in project root. If needed, copy its shortcut to a desired location."
Write-Host ""

# Setup session env variables. Once the tests complete, the env variables are auto-cleaned up
$envScript = Join-Path $PSScriptRoot 'config\setup_session_env_variables.ps1'

# Executes the envScript in the same PowerShell process so that the env variables are accessible to tests
if (Test-Path $envScript) {
    Write-Host "Setting up env variables ..."
    & $envScript
} else {
    Write-Host "ERROR: config\setup_session_env_variables.ps1 not found. Setting up env variables is mandatory."
    Write-Host ""
    Write-Host "Press any key to close this window ..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}
Write-Host ""
Write-Host "Env variables setup completed."
Write-Host ""

# Config
$PYTHON_EXE = 'C:\Program Files\Python314\python.exe'

# Execute tests - pytest paramters are defined in pytest.ini
& $PYTHON_EXE -m pytest
$rc = $LASTEXITCODE

# Send report only for exit codes 0 (passed) and 1 (failed)
if ($rc -eq 0 -or $rc -eq 1) {
    & $PYTHON_EXE -m utilities.report
}
else {
    Write-Host "Pytest execution exited unexpectedly with exit code $rc. Report sending cancelled."
}

Write-Host ""
Write-Host "Press any key to close this window ..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

exit $rc
