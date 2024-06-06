from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def close_cookie_banner(driver: WebDriver) -> None:
    try:
        close_button = driver.find_element(
            By.CSS_SELECTOR,
            "button.ca-button.ca-secondary-button.ca-secondary-button-first.go241155495.ca-button-opt-in",
        )
        close_button.click()
    except Exception:
        pass


def setup_driver() -> WebDriver:
    load_dotenv()
    options: Options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")  # Disable GPU acceleration
    options.add_argument("--no-sandbox")  # Bypass OS security model
    service: ChromeService = ChromeService(
        executable_path=ChromeDriverManager().install()
    )
    driver: WebDriver = webdriver.Chrome(service=service, options=options)
    return driver
