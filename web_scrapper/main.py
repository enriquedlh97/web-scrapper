from scrappers.utils import setup_driver
from scrappers.audi.audi_scrapper import scrape_audi


def main() -> None:
    scrape_audi(setup_driver())


if __name__ == "__main__":
    main()
