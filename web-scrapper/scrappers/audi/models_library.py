from typing import Callable, TypeVar
from pydantic import BaseModel
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

T = TypeVar('T')


class Years(BaseModel):
    available_years: set[int]


class BodyStyles(BaseModel):
    available_styles: set[str]


class Models(BaseModel):
    available_models: set[str]


def get_li_elements_from_div(sidebar: WebElement, div_number: int):
    xpath: str = f"div[{div_number}]"
    div_element: WebElement = sidebar.find_element(By.XPATH, xpath)
    ul_element: WebElement = div_element.find_element(By.TAG_NAME, "ul")
    li_elements: list[WebElement] = ul_element.find_elements(By.TAG_NAME, "li")
    return li_elements


def get_items_from_div(sidebar: WebElement, div_number: int, converter: Callable[[str], T]) -> list[T]:
    li_elements = get_li_elements_from_div(sidebar, div_number)
    return [converter(li.text) for li in li_elements]


def get_years(sidebar: WebElement, div_number: int = 2) -> list[int]:
    return get_items_from_div(sidebar, div_number, int)


def get_styles(sidebar: WebElement, div_number: int = 4) -> list[str]:
    return get_items_from_div(sidebar, div_number, str)


def get_models(sidebar: WebElement, div_number: int = 5) -> list[str]:
    return get_items_from_div(sidebar, div_number, str)


def build_data(driver: WebDriver) -> tuple[Years, BodyStyles, Models]:
    sidebar: WebElement = driver.find_element(By.CLASS_NAME, "facets-container")

    years: Years = Years(available_years=set(get_years(sidebar)))
    body_styles: BodyStyles = BodyStyles(available_styles=set(get_styles(sidebar)))
    models: Models = Models(available_models=set(get_models(sidebar)))

    return years, body_styles, models
