from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Import project methods
from methods.methods_base import MethodsBase


class MethodsExternalUserLogin(MethodsBase):
    def input_user_id_textbox(self, user_id) -> None:
        # Input User Id
        user_id_textbox = (
            WebDriverWait(self.driver, 10)
            .until(EC.presence_of_element_located((By.CSS_SELECTOR, "main-element")))
            .shadow_root
            .find_element(By.CSS_SELECTOR, "login-page")
            .shadow_root
            .find_element(By.CSS_SELECTOR, "jha-form-text-input[data-auto-id='userIdInput']")
            .shadow_root
            .find_element(By.CSS_SELECTOR, "input[aria-label='User ID']")
        )
        user_id_textbox.clear()
        user_id_textbox.send_keys(user_id)

    def input_password_textbox(self, password) -> None:
        # Input Password
        (
            WebDriverWait(self.driver, 10)
            .until(EC.presence_of_element_located((By.CSS_SELECTOR, "main-element")))
            .shadow_root
            .find_element(By.CSS_SELECTOR, "login-page")
            .shadow_root
            .find_element(By.CSS_SELECTOR, "jha-form-input[data-auto-id='passwordInput']")
            .shadow_root
            .find_element(By.CSS_SELECTOR, "input[aria-label='Password']")
            .send_keys(password)
        )

    def click_login_button(self) -> None:
        # Click Login button
        (
            WebDriverWait(self.driver, 10)
            .until(EC.presence_of_element_located((By.CSS_SELECTOR, "main-element")))
            .shadow_root
            .find_element(By.CSS_SELECTOR, "login-page")
            .shadow_root
            .find_element(By.CSS_SELECTOR, "jha-button[data-auto-id='submitBtn']")
            .click()
        )

    def input_verification_code_textbox(self, otp) -> None:
        # Input Verification Code
        (
            WebDriverWait(self.driver, 10)
            .until(EC.presence_of_element_located((By.CSS_SELECTOR, "main-element")))
            .shadow_root
            .find_element(By.CSS_SELECTOR, "login-page")
            .shadow_root
            .find_element(By.CSS_SELECTOR, "multi-factor-auth")
            .shadow_root
            .find_element(By.CSS_SELECTOR, "jha-form-input[data-auto-id='authInput']")
            .shadow_root
            .find_element(By.CSS_SELECTOR, "input[aria-label='Verification Code']")
            .send_keys(otp)
        )

    def click_verify_button(self) -> None:
        # Click Verify button
        (
            WebDriverWait(self.driver, 10)
            .until(EC.presence_of_element_located((By.CSS_SELECTOR, "main-element")))
            .shadow_root
            .find_element(By.CSS_SELECTOR, "login-page")
            .shadow_root
            .find_element(By.CSS_SELECTOR, "multi-factor-auth")
            .shadow_root
            .find_element(By.CSS_SELECTOR, "jha-button[data-auto-id='verifyBtn']")
            .click()
        )
