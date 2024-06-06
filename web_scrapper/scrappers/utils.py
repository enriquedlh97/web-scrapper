from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager


def setup_driver() -> WebDriver:
    options: Options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")  # Disable GPU acceleration
    options.add_argument("--no-sandbox")  # Bypass OS security model
    service: ChromeService = ChromeService(
        executable_path=ChromeDriverManager().install()
    )
    driver: WebDriver = webdriver.Chrome(service=service, options=options)
    return driver
