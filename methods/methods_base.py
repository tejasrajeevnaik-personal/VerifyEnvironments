from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import TimeoutException


class MethodsBase:
    def __init__(self, driver):
        self.driver = driver

    def open(self, url):
        self.driver.get(url)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

    def is_logged_in(self, timeout) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(EC.url_contains("/users"))
            return True
        except TimeoutException:
            return False
