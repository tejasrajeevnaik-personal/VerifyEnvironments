import pytest
from time import sleep

# Import project config
from config.config import Config

# Import project utilities
from utilities.driver_factory import DriverFactory

# Import project methods
from methods.methods_okta_login import MethodsOktaLogin


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
        print("Okta login to {} environment succeeded.".format(env))
        return
    if login.is_okta_logged_in(10):
        login.click_first_select_button()
        if login.is_logged_in(10):
            assert True
            print("Okta login to {} environment succeeded.".format(env))
            return
        else:
            print("Okta login to {} environment failed.".format(env))
            assert False
    login.input_jh_email_address_textbox()
    login.check_keep_me_signed_in_checkbox()
    login.click_next_button()
    login.click_select_for_password_button()
    login.input_jh_email_password_textbox()
    login.click_verify_button()
    login.click_select_for_okta_button()
    # User manually inputs the Okta code and hits ENTER key
    login.click_first_select_button()
    if login.is_logged_in(120):
        assert True
        print("Okta login to {} environment succeeded.".format(env))
        sleep(5)  # Wait for end user to see
        return
    else:
        print("Okta login to {} environment failed.".format(env))
        sleep(5)  # Wait for end user to see
        assert False
