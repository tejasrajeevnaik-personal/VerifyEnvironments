import pytest
from time import sleep

# Import project configs
from configs.config import Config

# Import project utilities
from utilities.driver_factory import DriverFactory
from utilities.otp import OTP
from utilities.logger import get_logger

# Import project methods
from methods.methods_external_user_login import MethodsExternalUserLogin

# Get module-level logger
logger = get_logger(__name__)


@pytest.fixture(scope="function")
def login(request):
    driver = DriverFactory.open_driver(Config.browser)
    login = MethodsExternalUserLogin(driver)
    yield login
    DriverFactory.close_driver(driver)


@pytest.mark.display_name("External user login - DEV env")
def test_dev(login):
    external_user_login(login,
                        "dev",
                        Config.dev_url,
                        Config.dev_external_user_id,
                        Config.dev_external_password)


@pytest.mark.display_name("External user login - DEV-INT env")
def test_dev_int(login):
    external_user_login(login,
                        "dev-int",
                        Config.dev_int_url,
                        Config.dev_int_external_user_id,
                        Config.dev_int_external_password)


@pytest.mark.display_name("External user login - TEST env")
def test_test(login):
    external_user_login(login,
                        "test",
                        Config.test_url,
                        Config.test_external_user_id,
                        Config.test_external_password)


@pytest.mark.display_name("External user login - STAGING env")
def test_staging(login):
    external_user_login(login,
                        "staging",
                        Config.staging_url,
                        Config.staging_external_user_id,
                        Config.staging_external_password)


def external_user_login(login, env, url, user_id, password):
    login.open(url)
    login.input_user_id_textbox(user_id)
    login.input_password_textbox(password)
    login.click_login_button()
    if not login.is_verification_code_textbox(20):
        message = f"External user login to {env} environment failed - "\
                  f"didn't navigate to MFA page"
        logger.error(message)
        raise message
    otp = OTP.get_otp_from_gmail_imap(
        Config.external_gmail_address,
        Config.external_gmail_app_password,
        Config.external_otp_email_subject_filter,
        90,
        5.0,
        True
    )
    if not otp:
        message = f"External user login to {env} environment failed - OTP not found."
        logger.error(message)
        raise message
    login.input_verification_code_textbox(otp)
    login.click_verify_button()
    if login.is_logged_in(30):
        assert True
        logger.info("External user login to %s environment succeeded.", env)
        sleep(1)  # Wait for end user to see
        return
    else:
        assert_message = f"External user login to {env} environment failed - graceful landing failed."
        logger.error(assert_message)
        sleep(1)  # Wait for end user to see
        assert False, assert_message
