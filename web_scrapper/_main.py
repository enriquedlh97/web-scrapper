import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


# Function to set up the Selenium web driver
def setup_driver():
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")  # Disable GPU acceleration
    options.add_argument("--no-sandbox")  # Bypass OS security model
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver


# Function to extract data from the first URL (Audi Gainesville)
def extract_data_audi(driver):
    driver.get(
        "https://www.audigainesville.com/global-incentives-search/index.htm?ddcref=tier1_offers"
    )

    # Example selectors, replace these with actual selectors from the page
    audience_model = driver.find_element(
        By.CSS_SELECTOR, "selector_for_audience_model"
    ).text
    make = driver.find_element(By.CSS_SELECTOR, "selector_for_make").text
    model = driver.find_element(By.CSS_SELECTOR, "selector_for_model").text
    trim = driver.find_element(By.CSS_SELECTOR, "selector_for_trim").text
    year = driver.find_element(By.CSS_SELECTOR, "selector_for_year").text
    condition = driver.find_element(By.CSS_SELECTOR, "selector_for_condition").text
    type_ = driver.find_element(By.CSS_SELECTOR, "selector_for_type").text

    offer_settings = {
        "payment": driver.find_element(By.CSS_SELECTOR, "selector_for_payment").text
        or None,
        "payment_label": driver.find_element(
            By.CSS_SELECTOR, "selector_for_payment_label"
        ).text
        or None,
        "term": driver.find_element(By.CSS_SELECTOR, "selector_for_term").text or None,
        "down_payment": driver.find_element(
            By.CSS_SELECTOR, "selector_for_down_payment"
        ).text
        or None,
        "down_payment_label": driver.find_element(
            By.CSS_SELECTOR, "selector_for_down_payment_label"
        ).text
        or None,
        "expiration": driver.find_element(
            By.CSS_SELECTOR, "selector_for_expiration"
        ).text,
        "price": driver.find_element(By.CSS_SELECTOR, "selector_for_price").text
        or None,
        "disclaimer": driver.find_element(
            By.CSS_SELECTOR, "selector_for_disclaimer"
        ).text,
        "apr": driver.find_element(By.CSS_SELECTOR, "selector_for_apr").text or None,
        "name": driver.find_element(By.CSS_SELECTOR, "selector_for_name").text or None,
        "amount": driver.find_element(By.CSS_SELECTOR, "selector_for_amount").text
        or None,
        "free_text": driver.find_element(By.CSS_SELECTOR, "selector_for_free_text").text
        or None,
        "vin": driver.find_element(By.CSS_SELECTOR, "selector_for_vin").text or None,
        "msrp": float(
            driver.find_element(By.CSS_SELECTOR, "selector_for_msrp")
            .text.replace("$", "")
            .replace(",", "")
        )
        or None,
    }

    data = {
        "audience_model": audience_model,
        "make": make,
        "model": model,
        "trim": trim,
        "year": year,
        "condition": condition,
        "type": type_,
        "offer_settings": offer_settings,
    }

    return data


# Function to extract data from the second URL (Mini USA)
def extract_data_mini(driver):
    driver.get("https://www.miniusa.com/inventory.html#/results")

    # Example selectors, replace these with actual selectors from the page
    audience_model = driver.find_element(
        By.CSS_SELECTOR, "selector_for_audience_model"
    ).text
    make = driver.find_element(By.CSS_SELECTOR, "selector_for_make").text
    model = driver.find_element(By.CSS_SELECTOR, "selector_for_model").text
    trim = driver.find_element(By.CSS_SELECTOR, "selector_for_trim").text
    year = driver.find_element(By.CSS_SELECTOR, "selector_for_year").text
    condition = driver.find_element(By.CSS_SELECTOR, "selector_for_condition").text
    type_ = driver.find_element(By.CSS_SELECTOR, "selector_for_type").text

    offer_settings = {
        "payment": driver.find_element(By.CSS_SELECTOR, "selector_for_payment").text
        or None,
        "payment_label": driver.find_element(
            By.CSS_SELECTOR, "selector_for_payment_label"
        ).text
        or None,
        "term": driver.find_element(By.CSS_SELECTOR, "selector_for_term").text or None,
        "down_payment": driver.find_element(
            By.CSS_SELECTOR, "selector_for_down_payment"
        ).text
        or None,
        "down_payment_label": driver.find_element(
            By.CSS_SELECTOR, "selector_for_down_payment_label"
        ).text
        or None,
        "expiration": driver.find_element(
            By.CSS_SELECTOR, "selector_for_expiration"
        ).text,
        "price": driver.find_element(By.CSS_SELECTOR, "selector_for_price").text
        or None,
        "disclaimer": driver.find_element(
            By.CSS_SELECTOR, "selector_for_disclaimer"
        ).text,
        "apr": driver.find_element(By.CSS_SELECTOR, "selector_for_apr").text or None,
        "name": driver.find_element(By.CSS_SELECTOR, "selector_for_name").text or None,
        "amount": driver.find_element(By.CSS_SELECTOR, "selector_for_amount").text
        or None,
        "free_text": driver.find_element(By.CSS_SELECTOR, "selector_for_free_text").text
        or None,
        "vin": driver.find_element(By.CSS_SELECTOR, "selector_for_vin").text or None,
        "msrp": float(
            driver.find_element(By.CSS_SELECTOR, "selector_for_msrp")
            .text.replace("$", "")
            .replace(",", "")
        )
        or None,
    }

    data = {
        "audience_model": audience_model,
        "make": make,
        "model": model,
        "trim": trim,
        "year": year,
        "condition": condition,
        "type": type_,
        "offer_settings": offer_settings,
    }

    return data


# Main function
def main():
    urls = [
        (
            "https://www.audigainesville.com/global-incentives-search/index.htm?ddcref=tier1_offers",
            extract_data_audi,
        ),
        ("https://www.miniusa.com/inventory.html#/results", extract_data_mini),
    ]

    driver = setup_driver()
    results = []

    for url, extract_function in urls:
        try:
            data = extract_function(driver)
            results.append(data)
            break  # Stop after first successful extraction
        except Exception as e:
            print(f"Failed to extract data from {url}: {e}")
            continue

    driver.quit()

    # Output the results as JSON
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
