from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By


def close_cookie_banner(driver: WebDriver) -> None:
    try:
        close_button = driver.find_element(
            By.CSS_SELECTOR,
            "button.ca-button.ca-secondary-button.ca-secondary-button-first.go241155495.ca-button-opt-in",  # noqa: E501
        )
        close_button.click()
    except Exception:
        pass
