import logging
import re
from typing import Iterable

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from web_scrapper.scrappers.audi.extractor_agent.offer_extractor_agent import (
    extract_offer_info,
)
from web_scrapper.scrappers.audi.models_library import (
    BodyStyles,
    Models,
    Offer,
    OfferSettings,
    Years,
    build_data,
)
from web_scrapper.scrappers.audi.utils import close_cookie_banner
from web_scrapper.settings import AUDI_URL


def get_offer_types(
    main_content: WebElement,
) -> tuple[list[WebElement], list[WebElement]]:
    finance_offers: list[WebElement] = []
    promotion_offers: list[WebElement] = []

    try:
        finance_offers: list[WebElement] = main_content.find_element(
            By.CSS_SELECTOR, 'section[data-offer="APR"]'
        ).find_elements(By.TAG_NAME, "article")
    except Exception:
        logging.info("No finance offers found")

    try:
        promotion_offers: list[WebElement] = main_content.find_element(
            By.CSS_SELECTOR, 'section[data-offer="PROMOTION"]'
        ).find_elements(By.TAG_NAME, "article")
    except Exception:
        logging.info("No promotion offers found")

    return finance_offers, promotion_offers


def get_offers(model: WebElement, driver: WebDriver) -> list[OfferSettings]:
    model.find_element(By.XPATH, "a[2]").click()
    close_cookie_banner(driver)
    main_content: WebElement = driver.find_element(
        By.CLASS_NAME, "ddc-wrapper"
    ).find_element(By.XPATH, "div[2]")

    offer_types: tuple[list[WebElement], list[WebElement]] = get_offer_types(
        main_content
    )

    offers: dict[str, list[WebElement]] = {
        "finance_offers": offer_types[0],
        "promotion_offers": offer_types[1],
    }

    extracted_offers: list[OfferSettings] = []
    for offer_type, offers_list in offers.items():
        if not offers_list:
            continue

        for offer in offers_list:
            extracted_offers.append(extract_offer_info(offer.text, offer_type))

    return extracted_offers


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


def get_all_models(driver: WebDriver) -> list[WebElement]:
    all_models: list[WebElement] = driver.find_element(
        By.CLASS_NAME, "vehicles-container"
    ).find_elements(By.CLASS_NAME, "vehicle-container")

    return all_models


def get_all_offers(
    driver: WebDriver,
    years: Years,
    styles: BodyStyles,
    models: Models,
    expected_models_count: int,
) -> list[Offer]:
    all_models: list[WebElement] = get_all_models(driver)

    assert (
        len(all_models) == expected_models_count
    ), "Did not find the correct number of models"

    offers_data: list[Offer] = []
    for model_idx in range(expected_models_count):
        model_name: str = all_models[model_idx].find_element(By.TAG_NAME, "h5").text
        logging.info(f"Getting all offers for: {model_name}")

        offer: Offer = Offer(
            audience_model=model_name,
            model=extract_model_from_string(models, input_string=model_name),
            trim=extract_trim_from_string(styles, input_string=model_name),
            year=extract_year_from_string(years, input_string=model_name),
        )

        extracted_offers: list[OfferSettings] = get_offers(all_models[model_idx], driver)

        for extracted_offer in extracted_offers:
            new_offer: Offer = offer.model_copy()
            new_offer.offer_settings = extracted_offer
            offers_data.append(new_offer)

        driver.back()
        # Refresh all models
        all_models = get_all_models(driver)

        assert (
            len(all_models) == expected_models_count
        ), "Did not find the correct number of models"
        close_cookie_banner(driver)

    return offers_data


def scrape_audi(driver: WebDriver, url: str = AUDI_URL) -> list[Offer]:
    driver.get(url)
    close_cookie_banner(driver)
    years, styles, models = build_data(driver)
    offers: list[Offer] = get_all_offers(
        driver, years, styles, models, get_models_count(driver)
    )
    logging.info("Quitting Driver")
    driver.quit()

    return offers
