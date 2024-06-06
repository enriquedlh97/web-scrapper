from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager


def setup_driver() -> WebDriver:
    load_dotenv()
    options: Options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    service: ChromeService = ChromeService(
        executable_path=ChromeDriverManager().install()
    )
    driver: WebDriver = webdriver.Chrome(service=service, options=options)
    return driver
