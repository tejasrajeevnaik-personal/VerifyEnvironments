<#
Important: This file should always reside in project root.
Usage: This script is specifically written to be invoked by pipeline for CI/CD automation. It expects that:
1. all secrets are stored in pipeline secret store (GitHub or Azure Pipelines) and
2. pipeline sets the secrets to env variables before invoking this ps1 script
#>

Write-Host "Running VerifyEnvironments CI pipeline ..."
Write-Host ""

# Validate all required env variables are present
$requiredSecrets = @(
    "EFM_BROWSER",
    "EFM_BROWSER_HEADLESS",

    "EFM_DEV_URL",
    "EFM_DEV_TFS_HOST",
    "EFM_DEV_EXTERNAL_USER_ID",
    "EFM_DEV_EXTERNAL_PASSWORD",
    "EFM_DEV_PARTICIPANT_PASSWORD_USER_ID",
    "EFM_DEV_PARTICIPANT_PASSWORD_PASSWORD",
    "EFM_DEV_PARTICIPANT_SSH_USER_ID",
    "EFM_DEV_PARTICIPANT_SSH_KEY",

    "EFM_DEV_INT_URL",
    "EFM_DEV_INT_TFS_HOST",
    "EFM_DEV_INT_EXTERNAL_USER_ID",
    "EFM_DEV_INT_EXTERNAL_PASSWORD",
    "EFM_DEV_INT_PARTICIPANT_PASSWORD_USER_ID",
    "EFM_DEV_INT_PARTICIPANT_PASSWORD_PASSWORD",
    "EFM_DEV_INT_PARTICIPANT_SSH_USER_ID",
    "EFM_DEV_INT_PARTICIPANT_SSH_KEY",

    "EFM_TEST_URL",
    "EFM_TEST_TFS_HOST",
    "EFM_TEST_EXTERNAL_USER_ID",
    "EFM_TEST_EXTERNAL_PASSWORD",
    "EFM_TEST_PARTICIPANT_PASSWORD_USER_ID",
    "EFM_TEST_PARTICIPANT_PASSWORD_PASSWORD",
    "EFM_TEST_PARTICIPANT_SSH_USER_ID",
    "EFM_TEST_PARTICIPANT_SSH_KEY",

    "EFM_STAGING_URL",
    "EFM_STAGING_TFS_HOST",
    "EFM_STAGING_EXTERNAL_USER_ID",
    "EFM_STAGING_EXTERNAL_PASSWORD",
    "EFM_STAGING_PARTICIPANT_PASSWORD_USER_ID",
    "EFM_STAGING_PARTICIPANT_PASSWORD_PASSWORD",
    "EFM_STAGING_PARTICIPANT_SSH_USER_ID",
    "EFM_STAGING_PARTICIPANT_SSH_KEY",

    "EFM_OKTA_JH_EMAIL_ADDRESS",
    "EFM_OKTA_JH_EMAIL_PASSWORD",
    "EFM_OKTA_JH_EMAIL_TOTP_SECRET",

    "EFM_EXTERNAL_GMAIL_ADDRESS",
    "EFM_EXTERNAL_GMAIL_APP_PASSWORD",
    "EFM_EXTERNAL_OTP_EMAIL_SUBJECT_FILTER",

    "EFM_SEND_REPORT_GMAIL",
    "EFM_SEND_REPORT_EMAIL_APP_PASSWORD",
    "EFM_SEND_REPORT_SUBJECT_PREFIX",
    "EFM_SEND_REPORT_RECIPIENTS"
)

$missing = @()

foreach ($secret in $requiredSecrets)
{
    $value = [System.Environment]::GetEnvironmentVariable($secret)
    if (-not $value)
    {
        $missing += $secret
    }
}

if ($missing.Count -gt 0)
{
    Write-Host "Error: Missing required environment variables:" -ForegroundColor Red
    $missing | ForEach-Object { Write-Host " - $_" -ForegroundColor Red }
    exit 1
}

Write-Host "All required environment variables found."
Write-Host ""

# Python and the required packages are expected to be installed in pipeline before invoking this ps1 script
$PYTHON_EXE = "python"

# Run tests
Write-Host "Running pytest ..."
& $PYTHON_EXE -m pytest
$rc = $LASTEXITCODE

# Generate and send report
if ($rc -eq 0 -or $rc -eq 1)
{
    Write-Host "Generating and sending report ..."
    & $PYTHON_EXE -m reports.report
}
else
{
    Write-Host "Pytest execution exited unexpectedly with exit code $rc. Skipping report."
}

exit $rc
