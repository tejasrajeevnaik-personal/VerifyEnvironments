import pytest
from time import sleep

# Import project config
from config.config import Config

# Import project utilities
from utilities.driver_factory import DriverFactory
from utilities.otp import OTP

# Import project methods
from methods.methods_external_user_login import MethodsExternalUserLogin


@pytest.fixture(scope="function")
def login(request):
    driver = DriverFactory.open_driver(Config.browser)
    login = MethodsExternalUserLogin(driver)
    yield login
    DriverFactory.close_driver(driver)


def test_dev(login):
    external_user_login(login,
                        "dev",
                        Config.dev_url,
                        Config.dev_external_user_id,
                        Config.dev_external_password)

def test_dev_int(login):
    external_user_login(login,
                        "dev-int",
                        Config.dev_int_url,
                        Config.dev_int_external_user_id,
                        Config.dev_int_external_password)

def test_staging(login):
    external_user_login(login,
                        "staging",
                        Config.staging_url,
                        Config.staging_external_user_id,
                        Config.staging_external_password)

def test_test(login):
    external_user_login(login,
                        "test",
                        Config.test_url,
                        Config.test_external_user_id,
                        Config.test_external_password)

def external_user_login(login, env, url, user_id, password):
    login.open(url)
    login.input_user_id_textbox(user_id)
    login.input_password_textbox(password)
    login.click_login_button()
    otp = OTP.get_otp_from_gmail_imap(
        Config.gmail_address,
        Config.gmail_app_password,
        Config.otp_email_subject_filter,
        120,
        5.0,
        True
    )
    if not otp:
        raise AssertionError("OTP not found")
    login.input_verification_code_textbox(otp)
    login.click_verify_button()
    if login.is_logged_in(30):
        assert True
        print("External user login to {} environment succeeded.".format(env))
        sleep(5) # Wait for end user to see
        return
    else:
        print("External user login to {} environment failed.".format(env))
        sleep(5)  # Wait for end user to see
        assert False
