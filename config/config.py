import os
from dataclasses import dataclass
from typing import List

# Import project utilities
from utilities.logger import get_logger

# Get module-level logger
logger = get_logger(__name__)


# Mask secret: This helps NOT to expose the secrets in logging / output / reports
class Secret(str):
    def __repr__(self) -> str:
        return "*****"


# Fetch secret value from environment variables. Raises at import time if missing to stop the execution
def __get_secret(env_variable_name: str) -> Secret:
    value = os.getenv(env_variable_name)
    if value is None:
        message = f"Missing required environment variable: {env_variable_name}"
        logger.exception(message)
        raise RuntimeError(message)
    return Secret(value)


# Fetch non-secret value from environment variables. Raises at import time if missing to stop the execution
def __get_value(env_variable_name: str, default_value: str = None) -> str:
    value = os.getenv(env_variable_name)
    if value is None and default_value is None:
        message = f"Missing required environment variable: {env_variable_name}"
        logger.exception(message)
        raise RuntimeError(message)
    elif value is None and default_value is not None:
        value = default_value
    return value


# Freeze the class to avoid accidental assignments to config variables
@dataclass(frozen=True)
class __Config:
    # Browser
    browser: str

    # Environments config - DEV env
    dev_url: Secret
    dev_tfs_host: Secret
    dev_external_user_id: str
    dev_external_password: Secret
    dev_participant_password_user_id: str
    dev_participant_password_password: Secret
    dev_participant_ssh_user_id: str
    dev_participant_ssh_key: Secret

    # Environments config - DEV-INT env
    dev_int_url: Secret
    dev_int_tfs_host: Secret
    dev_int_external_user_id: str
    dev_int_external_password: Secret
    dev_int_participant_password_user_id: str
    dev_int_participant_password_password: Secret
    dev_int_participant_ssh_user_id: str
    dev_int_participant_ssh_key: Secret

    # Environments config - TEST env
    test_url: Secret
    test_tfs_host: Secret
    test_external_user_id: str
    test_external_password: Secret
    test_participant_password_user_id: str
    test_participant_password_password: Secret
    test_participant_ssh_user_id: str
    test_participant_ssh_key: Secret

    # Environments config - STAGING env
    staging_url: Secret
    staging_tfs_host: Secret
    staging_external_user_id: str
    staging_external_password: Secret
    staging_participant_password_user_id: str
    staging_participant_password_password: Secret
    staging_participant_ssh_user_id: str
    staging_participant_ssh_key: Secret

    # Okta user login config
    okta_jh_email_address: Secret
    okta_jh_email_password: Secret

    # OTP retrieval for external user login config
    external_gmail_address: str
    external_gmail_app_password: Secret
    external_otp_email_subject_filter: str

    # Send report config
    send_report_gmail: str
    send_report_gmail_app_password: Secret
    send_report_gmail_smtp_host: str
    send_report_gmail_smtp_port: int
    send_report_subject_prefix: str
    send_report_recipients: List[str]


# Frozen instance which is accessed throughout the project
Config = __Config(
    # Browser
    browser=__get_value("EFM_BROWSER",
                        "chrome"),

    # Environments config - DEV env
    dev_url=__get_secret("EFM_DEV_URL"),
    dev_tfs_host=__get_secret("EFM_DEV_TFS_HOST"),
    dev_external_user_id=__get_value("EFM_DEV_EXTERNAL_USER_ID",
                                     "tejasrajeevnaiktesting"),
    dev_external_password=__get_secret("EFM_DEV_EXTERNAL_PASSWORD"),
    dev_participant_password_user_id=__get_value("EFM_DEV_PARTICIPANT_PASSWORD_USER_ID",
                                                 "tejas_naik_pa_password"),
    dev_participant_password_password=__get_secret("EFM_DEV_PARTICIPANT_PASSWORD_PASSWORD"),
    dev_participant_ssh_user_id=__get_value("EFM_DEV_PARTICIPANT_SSH_USER_ID",
                                            "tejas_naik_pa_ssh"),
    dev_participant_ssh_key=__get_secret("EFM_DEV_PARTICIPANT_SSH_KEY"),

    # Environments config - DEV-INT env
    dev_int_url=__get_secret("EFM_DEV_INT_URL"),
    dev_int_tfs_host=__get_secret("EFM_DEV_INT_TFS_HOST"),
    dev_int_external_user_id=__get_value("EFM_DEV_INT_EXTERNAL_USER_ID",
                                         "tejasrajeevnaiktesting"),
    dev_int_external_password=__get_secret("EFM_DEV_INT_EXTERNAL_PASSWORD"),
    dev_int_participant_password_user_id=__get_value("EFM_DEV_INT_PARTICIPANT_PASSWORD_USER_ID",
                                                     "tejas_naik_pa_password"),
    dev_int_participant_password_password=__get_secret("EFM_DEV_INT_PARTICIPANT_PASSWORD_PASSWORD"),
    dev_int_participant_ssh_user_id=__get_value("EFM_DEV_INT_PARTICIPANT_SSH_USER_ID",
                                                "tejas_naik_pa_ssh"),
    dev_int_participant_ssh_key=__get_secret("EFM_DEV_INT_PARTICIPANT_SSH_KEY"),

    # Environments config - TEST env
    test_url=__get_secret("EFM_TEST_URL"),
    test_tfs_host=__get_secret("EFM_TEST_TFS_HOST"),
    test_external_user_id=__get_value("EFM_TEST_EXTERNAL_USER_ID",
                                      "tejasrajeevnaiktesting"),
    test_external_password=__get_secret("EFM_TEST_EXTERNAL_PASSWORD"),
    test_participant_password_user_id=__get_value("EFM_TEST_PARTICIPANT_PASSWORD_USER_ID",
                                                  "tejas_naik_pa_password"),
    test_participant_password_password=__get_secret("EFM_TEST_PARTICIPANT_PASSWORD_PASSWORD"),
    test_participant_ssh_user_id=__get_value("EFM_TEST_PARTICIPANT_SSH_USER_ID",
                                             "tejas_naik_pa_ssh"),
    test_participant_ssh_key=__get_secret("EFM_TEST_PARTICIPANT_SSH_KEY"),

    # Environments config - STAGING env
    staging_url=__get_secret("EFM_STAGING_URL"),
    staging_tfs_host=__get_secret("EFM_STAGING_TFS_HOST"),
    staging_external_user_id=__get_value("EFM_STAGING_EXTERNAL_USER_ID",
                                         "tejasrajeevnaiktesting"),
    staging_external_password=__get_secret("EFM_STAGING_EXTERNAL_PASSWORD"),
    staging_participant_password_user_id=__get_value("EFM_STAGING_PARTICIPANT_PASSWORD_USER_ID",
                                                     "tejas_naik_pa_password"),
    staging_participant_password_password=__get_secret("EFM_STAGING_PARTICIPANT_PASSWORD_PASSWORD"),
    staging_participant_ssh_user_id=__get_value("EFM_STAGING_PARTICIPANT_SSH_USER_ID",
                                                "tejas_naik_pa_ssh"),
    staging_participant_ssh_key=__get_secret("EFM_STAGING_PARTICIPANT_SSH_KEY"),

    # Okta user login config
    okta_jh_email_address=__get_secret("EFM_JH_EMAIL_ADDRESS"),
    okta_jh_email_password=__get_secret("EFM_JH_EMAIL_PASSWORD"),

    # OTP retrieval for external user login config
    external_gmail_address=__get_value("EFM_GMAIL_ADDRESS"),
    external_gmail_app_password=__get_secret("EFM_GMAIL_APP_PASSWORD"),
    external_otp_email_subject_filter=__get_value("EFM_OTP_EMAIL_SUBJECT_FILTER",
                                                  "EFM OTP Code Verification"),

    # Send report config
    send_report_gmail=__get_value("EFM_SEND_REPORT_GMAIL",
                                  "tejasrajeevnaiktesting@gmail.com"),
    send_report_gmail_app_password=__get_secret("EFM_SEND_REPORT_EMAIL_APP_PASSWORD"),
    send_report_gmail_smtp_host="smtp.gmail.com",
    send_report_gmail_smtp_port=465,
    send_report_subject_prefix=__get_value("EFM_SEND_REPORT_SUBJECT_PREFIX",
                                           "[EFM envs] Automated Login verification tests"),
    send_report_recipients=[email.strip()
                            for email in __get_value("EFM_SEND_REPORT_RECIPIENTS",
                                                     "tejasrajeevnaik@live.com").split(",")]
)
