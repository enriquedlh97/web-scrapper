import json
import logging
from pathlib import Path

from web_scrapper.scrappers.audi.audi_scrapper import scrape_audi
from web_scrapper.scrappers.audi.models_library import Offer
from web_scrapper.scrappers.utils import setup_driver


def save_data(
    offers: list[Offer], output_file: Path = Path("extracted_offers.json")
) -> None:
    dict_list: list[dict] = [obj.model_dump() for obj in offers]
    with open(output_file, "w") as file:
        json.dump(dict_list, file, indent=4, default=str)

    logging.info(f"Extracted Offers saved to: {output_file}")


def main() -> None:
    offers: list[Offer] = scrape_audi(setup_driver())
    save_data(offers)


if __name__ == "__main__":
    main()
