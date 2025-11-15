<#
Important: This file should always reside in project root. If needed, copy its shortcut to a desired location.
Usage: Always open your IDE using this file. This ensures required env variables are setup which facilitates
debugging and running tests directly from IDE
Notes:
- Set $IDE to your desired IDE
- Accordingly set path for your IDE
#>

Write-Host "Important: This file should always reside in project root. If needed, copy its shortcut to a desired location."
Write-Host ""

# Choose IDE here: PyCharm, VSCode, or VSTS
$IDE = "PyCharm"

# Paths to IDE executables (edit to match your machine)
$PyCharmPath = "C:\Program Files\JetBrains\PyCharm 2025.2.3\bin\pycharm64.exe"
$VSCodePath = "C:\Users\YourUser\AppData\Local\Programs\Microsoft VS Code\Code.exe"
$VSTSPath = "C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\devenv.exe"

# Setup session env variables
. "$PSScriptRoot\config\setup_session_env_variables.ps1"

# Open selected IDE
switch ($IDE)
{
    "PyCharm" {
        if (-not (Test-Path $PyCharmPath))
        {
            Write-Host "PyCharm not found at path: $PyCharmPath" -ForegroundColor Red
            Write-Host "Please update the path or choose a different IDE."
            Write-Host "Press any key to continue ..."
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
            exit 1
        }
        & $PyCharmPath $PSScriptRoot
    }

    "VSCode" {
        if (-not (Test-Path $VSCodePath))
        {
            Write-Host "VS Code not found at path: $VSCodePath" -ForegroundColor Red
            Write-Host "Please update the path or choose a different IDE."
            Write-Host "Press any key to continue ..."
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
            exit 1
        }
        & $VSCodePath $PSScriptRoot
    }

    "VSTS" {
        if (-not (Test-Path $VSTSPath))
        {
            Write-Host "Visual Studio (VSTS) not found at path: $VSTSPath" -ForegroundColor Red
            Write-Host "Please update the path or choose a different IDE."
            Write-Host "Press any key to continue ..."
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
            exit 1
        }
        & $VSTSPath $PSScriptRoot
    }

    default {
        Write-Host "Unknown IDE value: $IDE" -ForegroundColor Red
        Write-Host "Use: PyCharm, VSCode, or VSTS."
        Write-Host "Press any key to continue ..."
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        exit 1
    }
}
