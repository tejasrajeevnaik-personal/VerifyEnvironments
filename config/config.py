class Config:
    browser: str = "edge"

    # Environment configs
    staging_url: str = "https://stg-filetransfer-ui.efm.jackhenry.com"
    staging_external_user_id: str = "tejasrajeevnaiktesting"
    staging_external_password: str = "mynameisFirstLast12!@"
    staging_participant_password_user_id: str = ""
    staging_participant_password_password: str = ""
    staging_participant_ssh_user_id: str = ""
    staging_participant_ssh_key: str = ""

    test_url: str = "https://test-filetransfer-ui.efm.jackhenry.com"
    test_external_user_id: str = "tejasrajeevnaiktesting"
    test_external_password: str = "mynameisFirstLast12!@"
    test_participant_password_user_id: str = ""
    test_participant_password_password: str = ""
    test_participant_ssh_user_id: str = ""
    test_participant_ssh_key: str = ""

    dev_url: str = "https://dev-filetransfer-ui.efm.jackhenry.com"
    dev_external_user_id: str = "tejasrajeevnaiktesting"
    dev_external_password: str = "mynameisFirstLast12!@"
    dev_participant_password_user_id: str = ""
    dev_participant_password_password: str = ""
    dev_participant_ssh_user_id: str = ""
    dev_participant_ssh_key: str = ""

    dev_int_url: str = "https://dev-int-filetransfer-ui.efm.jackhenry.com"
    dev_int_external_user_id: str = "tejasrajeevnaiktesting"
    dev_int_external_password: str = "mynameisFirstLast12!@"
    dev_int_participant_password_user_id: str = ""
    dev_int_participant_password_password: str = ""
    dev_int_participant_ssh_user_id: str = ""
    dev_int_participant_ssh_key: str = ""

    # Okta user login config
    jh_email_address: str = "tnaik@jhacorp.com"
    jh_email_password: str = "Khirad123!@#"

    # External user login config
    gmail_address: str = "tejasrajeevnaiktesting@gmail.com"
    gmail_app_password: str = "amjt szoj yrpb soaf"
    otp_email_subject_filter: str = "EFM OTP Code Verification"