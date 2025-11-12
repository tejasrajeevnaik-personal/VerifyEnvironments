from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import TimeoutException

# Import project config
from config.config import Config

# Import project methods
from methods.methods_base import MethodsBase


class MethodsOktaLogin(MethodsBase):
    def click_sso_with_okta_button(self) -> None:
        (
            WebDriverWait(self.driver, 10)
            .until(EC.presence_of_element_located((By.CSS_SELECTOR, "main-element")))
            .shadow_root
            .find_element(By.CSS_SELECTOR, "login-page")
            .shadow_root
            .find_element(By.CSS_SELECTOR, "jha-button[type='submit']")
            .click()
        )

    def is_okta_logged_in(self, timeout) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(EC.url_contains("/callback?code="))
            return True
        except TimeoutException:
            return False

    def click_okta_button(self) -> None:
        okta_button = (
            WebDriverWait(self.driver, 10)
            .until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label='OKTA']")))
        )
        self.driver.execute_script("arguments[0].click();", okta_button)

    def input_jh_email_address_textbox(self) -> None:
        jh_email_address_textbox = (
            WebDriverWait(self.driver, 10)
            .until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[autocomplete='username']")))
        )
        jh_email_address_textbox.clear()
        jh_email_address_textbox.send_keys(Config.jh_email_address)

    def check_keep_me_signed_in_checkbox(self) -> None:
        keep_me_signed_in_checkbox = (
            WebDriverWait(self.driver, 10)
            .until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='rememberMe']")))
        )
        self.driver.execute_script("arguments[0].click();", keep_me_signed_in_checkbox)

    def click_next_button(self) -> None:
        (
            WebDriverWait(self.driver, 10)
            .until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[value='Next']")))
            .click()
        )

    def click_select_for_password_button(self) -> None:
        (
            WebDriverWait(self.driver, 10)
            .until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[aria-label='Select Password.']")))
            .click()
        )

    def input_jh_email_password_textbox(self) -> None:
        (
            WebDriverWait(self.driver, 10)
            .until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='credentials.passcode']")))
            .send_keys(Config.jh_email_password)
        )

    def click_verify_button(self) -> None:
        (
            WebDriverWait(self.driver, 10)
            .until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[value='Verify']")))
            .click()
        )

    def click_select_for_okta_button(self) -> None:
        (
            WebDriverWait(self.driver, 10)
            .until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "a[aria-label='Select to enter a code from the Okta Verify app.']")))
            .click()
        )

    def click_for_user_id_select_button(self, user_id) -> None:
        select_button = (
            WebDriverWait(self.driver, 300)
            .until(EC.presence_of_element_located((By.CSS_SELECTOR, "main-element")))
            .shadow_root
            .find_element(By.CSS_SELECTOR, "callback-token")
            .shadow_root
            .find_element(By.CSS_SELECTOR, "jha-advanced-table")
            .shadow_root
            .find_element(By.CSS_SELECTOR, "button[title='{}'] > jha-button".format(user_id))
            .shadow_root
            .find_element(By.CSS_SELECTOR, "button[type='submit']")
        )
        self.driver.execute_script("arguments[0].click();", select_button)

    def click_first_select_button(self) -> None:
        first_select_button = (
            WebDriverWait(self.driver, 300)
            .until(EC.presence_of_element_located((By.CSS_SELECTOR, "main-element")))
            .shadow_root
            .find_element(By.CSS_SELECTOR, "callback-token")
            .shadow_root
            .find_element(By.CSS_SELECTOR, "jha-advanced-table")
            .shadow_root
            .find_element(By.CSS_SELECTOR, "#actionId > button > jha-button")
            .shadow_root
            .find_element(By.CSS_SELECTOR, "button[type='submit']")
        )
        self.driver.execute_script("arguments[0].click();", first_select_button)
