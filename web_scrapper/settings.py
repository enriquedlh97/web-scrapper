import logging
from typing import Final

from dotenv import load_dotenv

load_dotenv()

AUDI_URL: Final[
    str
] = "https://www.audigainesville.com/global-incentives-search/index.htm?ddcref=tier1_offers"  # noqa: E501

LLM_MODEL_NAME: Final[str] = "gpt-3.5-turbo-0125"


logging.basicConfig(level=logging.INFO)
