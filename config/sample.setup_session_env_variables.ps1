<#
Notes:
- On cloning the repo, make a copy of this file under same location and rename to setup_session_env_variables.ps1
- setup_session_env_variables.ps1 is git ignored so, you can safely put in secrets in it
- DO NOT accidentally put secrets in sample.setup_session_env_variables.ps1 and commit. It will expose the secrets
to the world
#>

# Browser
$env:EFM_BROWSER = "chrome"


# Environments config - DEV env
$env:EFM_DEV_URL = "https://dev.example.com"
$env:EFM_DEV_TFS_HOST = "dev-tfs-host"
$env:EFM_DEV_EXTERNAL_USER_ID = "dummy_external_user"
$env:EFM_DEV_EXTERNAL_PASSWORD = "dummy_password"
$env:EFM_DEV_PARTICIPANT_PASSWORD_USER_ID = "dummy_password_user"
$env:EFM_DEV_PARTICIPANT_PASSWORD_PASSWORD = "dummy_password"
$env:EFM_DEV_PARTICIPANT_SSH_USER_ID = "dummy_ssh_user"
# Paste the SSH key as it is from the Private key secret file. Make sure it trimmed at the start and end
$env:EFM_DEV_PARTICIPANT_SSH_KEY = @'
-----BEGIN RSA PRIVATE KEY-----
DUMMY-DEV-SSH-KEY
-----END RSA PRIVATE KEY-----
'@

# Environments config - DEV-INT env
$env:EFM_DEV_INT_URL = "https://dev-int.example.com"
$env:EFM_DEV_INT_TFS_HOST = "dev-int-tfs-host"
$env:EFM_DEV_INT_EXTERNAL_USER_ID = "dummy_external_user"
$env:EFM_DEV_INT_EXTERNAL_PASSWORD = "dummy_password"
$env:EFM_DEV_INT_PARTICIPANT_PASSWORD_USER_ID = "dummy_password_user"
$env:EFM_DEV_INT_PARTICIPANT_PASSWORD_PASSWORD = "dummy_password"
$env:EFM_DEV_INT_PARTICIPANT_SSH_USER_ID = "dummy_ssh_user"
# Paste the SSH key as it is from the Private key secret file. Make sure it trimmed at the start and end
$env:EFM_DEV_INT_PARTICIPANT_SSH_KEY = @'
-----BEGIN RSA PRIVATE KEY-----
DUMMY-DEV-INT-SSH-KEY
-----END RSA PRIVATE KEY-----
'@

# Environments config - TEST env
$env:EFM_TEST_URL = "https://test.example.com"
$env:EFM_TEST_TFS_HOST = "test-tfs-host"
$env:EFM_TEST_EXTERNAL_USER_ID = "dummy_external_user"
$env:EFM_TEST_EXTERNAL_PASSWORD = "dummy_password"
$env:EFM_TEST_PARTICIPANT_PASSWORD_USER_ID = "dummy_password_user"
$env:EFM_TEST_PARTICIPANT_PASSWORD_PASSWORD = "dummy_password"
$env:EFM_TEST_PARTICIPANT_SSH_USER_ID = "dummy_ssh_user"
# Paste the SSH key as it is from the Private key secret file. Make sure it trimmed at the start and end
$env:EFM_TEST_PARTICIPANT_SSH_KEY = @'
-----BEGIN RSA PRIVATE KEY-----
DUMMY-TEST-SSH-KEY
-----END RSA PRIVATE KEY-----
'@

# Environments config - STAGING env
$env:EFM_STAGING_URL = "https://staging.example.com"
$env:EFM_STAGING_TFS_HOST = "staging-tfs-host"
$env:EFM_STAGING_EXTERNAL_USER_ID = "dummy_external_user"
$env:EFM_STAGING_EXTERNAL_PASSWORD = "dummy_password"
$env:EFM_STAGING_PARTICIPANT_PASSWORD_USER_ID = "dummy_password_user"
$env:EFM_STAGING_PARTICIPANT_PASSWORD_PASSWORD = "dummy_password"
$env:EFM_STAGING_PARTICIPANT_SSH_USER_ID = "dummy_ssh_user"
# Paste the SSH key as it is from the Private key secret file. Make sure it trimmed at the start and end
$env:EFM_STAGING_PARTICIPANT_SSH_KEY = @'
-----BEGIN RSA PRIVATE KEY-----
DUMMY-STAGING-SSH-KEY
-----END RSA PRIVATE KEY-----
'@

# Okta user login config
$env:EFM_OKTA_JH_EMAIL_ADDRESS = "dummy_okta_user@example.com"
$env:EFM_OKTA_JH_EMAIL_PASSWORD = "dummy_okta_password"
$env:EFM_OKTA_JH_EMAIL_TOTP_SECRET = "dummy_secret"

# OTP retrieval for external user login config
$env:EFM_EXTERNAL_GMAIL_ADDRESS = "dummyuser@gmail.com"
$env:EFM_EXTERNAL_GMAIL_APP_PASSWORD = "dummy_app_password"
$env:EFM_EXTERNAL_OTP_EMAIL_SUBJECT_FILTER = "EFM OTP Code Verification"

# Send report config
$env:EFM_SEND_REPORT_GMAIL = "dummy_sender@gmail.com"
$env:EFM_SEND_REPORT_EMAIL_APP_PASSWORD = "dummy_sender_password"
$env:EFM_SEND_REPORT_SUBJECT_PREFIX = "[EFM envs] Automated Login verification tests"
$env:EFM_SEND_REPORT_RECIPIENTS = "recipient1@example.com,recipient2@example.com,recipient3@example.com"
