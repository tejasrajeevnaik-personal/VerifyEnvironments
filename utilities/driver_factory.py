import os
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService

# Import project configs
from configs.config import Config


class DriverFactory:
    @staticmethod
    def open_driver(browser: str = "edge") -> WebDriver:
        match browser.lower():
            case "edge":
                return DriverFactory.__get_edge_driver()
            case "chrome":
                return DriverFactory.__get_chrome_driver()
            case _:
                # Defaulting to Edge
                return DriverFactory.__get_edge_driver()

    @staticmethod
    def close_driver(driver) -> None:
        if driver:
            # noinspection PyBroadException
            try:
                driver.quit()
            except Exception:
                pass

    @staticmethod
    def __get_edge_driver():
        options = EdgeOptions()
        if Config.browser_headless:
            options.add_argument("--headless=new")
        # Windows: Discard driver logs
        options.add_argument("--log-level=3")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        # For Windows: use NUL, for others: /dev/null
        null_log = "NUL" if os.name == "nt" else "/dev/null"
        service = EdgeService(log_output=null_log)
        return webdriver.Edge(options=options, service=service)

    @staticmethod
    def __get_chrome_driver():
        options = ChromeOptions()
        if Config.browser_headless:
            options.add_argument("--headless=new")
        # Windows: Discard driver logs
        options.add_argument("--log-level=3")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        service = ChromeService(log_path="NUL")
        return webdriver.Chrome(options=options, service=service)
