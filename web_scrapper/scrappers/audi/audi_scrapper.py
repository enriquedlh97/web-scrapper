import re
from typing import Final, Iterable
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from scrappers.audi.models_library import Years, build_data, BodyStyles, Models


URL: Final[str] = "https://www.audigainesville.com/global-incentives-search/index.htm?ddcref=tier1_offers"
MAKE: Final[str] = "Audi"
AUDIENCE_MODEL: Final[None] = None
CONDITION: Final[None] = None
TYPE: Final[None] = None


def extract_pattern_from_string(patterns: Iterable[int | str], input_string: str) -> str | None:
    patterns_str = "|".join(map(str, patterns))
    match: re.Match[str] | None = re.search(rf'\b({patterns_str})\b', input_string)
    if match:
        matched_value: str = match.group(1)
        return matched_value
    return None


def extract_year_from_string(years: Years, input_string: str) -> int | None:
    year: str | None = extract_pattern_from_string(years.available_years, input_string)
    return int(year) if (year and year.isdigit()) else None


def extract_trim_from_string(styles: BodyStyles, input_string: str) -> str | None:
    return extract_pattern_from_string(styles.available_styles, input_string)


def get_models_count(driver: WebDriver) -> int:
    return int(driver.find_element(By.CLASS_NAME, "incentives-header").find_element(By.ID, "results-count").text)


def get_all_models(driver: WebDriver, years: Years, styles: BodyStyles, models: Models, expected_models_count: int | None = None):
    all_models: list[WebElement] = driver.find_element(By.CLASS_NAME, "vehicles-container").find_elements(By.CLASS_NAME, "vehicle-container")

    if expected_models_count:
        assert len(all_models) == expected_models_count


    output_data: dict = {}
    for model in all_models:
        model_data: dict[str, str | int | None] = {}

        model_name: str = model.find_element(By.TAG_NAME, "h5").text
        model_data["audience_model"] = AUDIENCE_MODEL
        model_data["make"] = MAKE
        model_data["model"] = model_name
        model_data["trim"] = extract_trim_from_string(styles, input_string=model_name)
        model_data["year"] = extract_year_from_string(years, input_string=model_name)
        # Trim = style
        model_data["condition"] = CONDITION
        model_data["type"] = TYPE

        print("")


def scrape_audi(driver: WebDriver, url: str = URL):
    driver.get(url)
    years, styles, models = build_data(driver)
    get_all_models(driver, years, styles, models, get_models_count(driver))
    print("")
