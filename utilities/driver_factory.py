from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions


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
            try: driver.quit()
            except: pass

    @staticmethod
    def __get_edge_driver():
        options = EdgeOptions()
        options.add_argument("--log-level=3")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        return webdriver.Edge(options=options)

    @staticmethod
    def __get_chrome_driver():
        options = ChromeOptions()
        options.add_argument("--log-level=3")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        return webdriver.Chrome(options=options)