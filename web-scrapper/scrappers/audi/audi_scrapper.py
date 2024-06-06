from typing import Final
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from scrappers.audi.models_library import build_data


URL: Final[str] = "https://www.audigainesville.com/global-incentives-search/index.htm?ddcref=tier1_offers"


def get_models_count(driver: WebDriver) -> int:
    return int(driver.find_element(By.CLASS_NAME, "incentives-header").find_element(By.ID, "results-count").text)


def get_all_models(driver: WebDriver, expected_models_count: int | None = None):
    all_models: list[WebElement] = driver.find_element(By.CLASS_NAME, "vehicles-container").find_elements(By.CLASS_NAME, "vehicle-container")

    if expected_models_count:
        assert len(all_models) == expected_models_count


    output_data: dict = {}
    for model in all_models:
        model_data: dict[str, str] = {}

        model_name: str = model.find_element(By.TAG_NAME, "h5").text
        model_data["model"] = model_name

    print("")


def scrape_audi(driver: WebDriver, url: str = URL):
    driver.get(url)
    years, styles, models = build_data(driver)
    get_all_models(driver, get_models_count(driver))
    print("")
