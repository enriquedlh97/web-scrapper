import re
from typing import Final, Iterable

from scrappers.audi.models_library import (BodyStyles, Models, OfferSettings,
                                           Years, build_data)
from scrappers.audi.offer_extractor_agent import extract_offer_info
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

URL: Final[
    str
] = "https://www.audigainesville.com/global-incentives-search/index.htm?ddcref=tier1_offers"
MAKE: Final[str] = "Audi"
CONDITION: Final[None] = None
TYPE: Final[None] = None


def get_offers(model: WebElement, driver: WebDriver) -> list[OfferSettings]:
    model.find_element(By.XPATH, "a[2]").click()
    main_content: WebElement = driver.find_element(
        By.CLASS_NAME, "ddc-wrapper"
    ).find_element(By.XPATH, "div[2]")

    offers: dict[str, list[WebElement]] = {
        "finance_offers": main_content.find_element(
            By.CSS_SELECTOR, 'section[data-offer="APR"]'
        ).find_elements(By.TAG_NAME, "article"),
        "promotion_offers": main_content.find_element(
            By.CSS_SELECTOR, 'section[data-offer="PROMOTION"]'
        ).find_elements(By.TAG_NAME, "article"),
    }

    for offer_type, offers_list in offers.items():
        if not offers_list:
            continue

        for offer in offers_list:
            parsed_offer: OfferSettings = extract_offer_info(offer.text)
        print("")

    print("")

    return []


def extract_pattern_from_string(
    patterns: Iterable[int | str], input_string: str
) -> str | None:
    patterns_str = "|".join(map(str, patterns))
    match: re.Match[str] | None = re.search(rf"\b({patterns_str})\b", input_string)
    if match:
        matched_value: str = match.group(1)
        return matched_value
    return None


def extract_year_from_string(years: Years, input_string: str) -> int | None:
    year: str | None = extract_pattern_from_string(years.available_years, input_string)
    return int(year) if (year and year.isdigit()) else None


def extract_trim_from_string(styles: BodyStyles, input_string: str) -> str | None:
    return extract_pattern_from_string(styles.available_styles, input_string)


def extract_model_from_string(models: Models, input_string: str) -> str | None:
    return extract_pattern_from_string(models.available_models, input_string)


def get_models_count(driver: WebDriver) -> int:
    return int(
        driver.find_element(By.CLASS_NAME, "incentives-header")
        .find_element(By.ID, "results-count")
        .text
    )


def get_all_models(
    driver: WebDriver,
    years: Years,
    styles: BodyStyles,
    models: Models,
    expected_models_count: int | None = None,
) -> list[dict[str, str | int | None | dict]]:
    all_models: list[WebElement] = driver.find_element(
        By.CLASS_NAME, "vehicles-container"
    ).find_elements(By.CLASS_NAME, "vehicle-container")

    if expected_models_count:
        assert len(all_models) == expected_models_count

    output_data: list[dict] = []
    for model in all_models[1:]:
        model_data: dict[str, str | int | None | dict] = {}

        model_name: str = model.find_element(By.TAG_NAME, "h5").text
        model_data["audience_model"] = model_name
        model_data["make"] = MAKE
        model_data["model"] = extract_model_from_string(models, input_string=model_name)
        model_data["trim"] = extract_trim_from_string(styles, input_string=model_name)
        model_data["year"] = extract_year_from_string(years, input_string=model_name)
        # Trim = style
        model_data["condition"] = CONDITION
        model_data["type"] = TYPE

        get_offers(model, driver)

        output_data.append(model_data)
    return output_data


def scrape_audi(driver: WebDriver, url: str = URL):
    driver.get(url)
    years, styles, models = build_data(driver)
    data = get_all_models(driver, years, styles, models, get_models_count(driver))
    print("")
