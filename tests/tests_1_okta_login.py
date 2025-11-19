import pytest
from time import sleep

# Import project configs
from configs.config import Config

# Import project utilities
from utilities.driver_factory import DriverFactory
from utilities.totp import TOTP
from utilities.logger import get_logger

# Import project methods
from methods.methods_okta_login import MethodsOktaLogin

# Get module-level logger
logger = get_logger(__name__)


@pytest.fixture(scope="module")
def login(request):
    driver = DriverFactory.open_driver(Config.browser)
    login = MethodsOktaLogin(driver)
    yield login
    DriverFactory.close_driver(driver)


@pytest.mark.display_name("Okta login - DEV env")
def test_dev(login):
    okta_login(login,
               "dev",
               Config.dev_url)


@pytest.mark.display_name("Okta login - DEV-INT env")
def test_dev_int(login):
    okta_login(login,
               "dev-int",
               Config.dev_int_url)


@pytest.mark.display_name("Okta login - TEST env")
def test_test(login):
    okta_login(login,
               "test",
               Config.test_url)


@pytest.mark.display_name("Okta login - STAGING env")
def test_staging(login):
    okta_login(login,
               "staging",
               Config.staging_url)


def okta_login(login, env, url):
    login.open(url)
    login.click_sso_with_okta_button()
    login.click_okta_button()
    if login.is_logged_in(10):
        assert True
        logger.info("Okta login to %s environment succeeded.",env)
        return
    if login.is_okta_logged_in(10):
        login.click_first_select_button()
        if login.is_logged_in(10):
            assert True
            logger.info("Okta login to %s environment succeeded.",env)
            return
        else:
            assert_message = f"Okta login to {env} environment failed - graceful landing failed."
            logger.error(assert_message)
            assert False, assert_message
    login.input_jh_email_address_textbox(Config.okta_jh_email_address)
    login.check_keep_me_signed_in_checkbox()
    login.click_next_button()
    login.click_select_for_password_button()
    login.input_jh_email_password_textbox(Config.okta_jh_email_password)
    login.click_verify_button()

    """
    # ----- Manual flow: User manually inputs the Okta code and hits ENTER key -----
    login.click_select_for_okta_button()
    # Manual code entry here
    # ----- End manual flow -----
    """
    # ----- Automated flow: Generate TOTP for Google authenticator and enter code -----
    login.click_select_for_google_authenticator_button()
    totp = TOTP.generate_totp()
    login.input_google_authenticator_code_textbox(totp)
    login.click_verify_button()
    # ----- End automated flow -----

    login.click_first_select_button()
    if login.is_logged_in(120):
        assert True
        logger.info("Okta login to %s environment succeeded.",env)
        sleep(1)  # Wait for end user to see
        return
    else:
        assert_message = f"Okta login to {env} environment failed - graceful landing failed."
        logger.error(assert_message)
        sleep(1)  # Wait for end user to see
        assert False, assert_message
