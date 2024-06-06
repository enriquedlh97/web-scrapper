import json

from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate)
from langchain.schema import BaseMessage, SystemMessage
from langchain_community.callbacks import get_openai_callback
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from web_scrapper.scrappers.audi.extractor_agent.prompts import (
    human_message_prompt_template_string, system_message_string)
from web_scrapper.scrappers.audi.models_library import OfferSettings
from web_scrapper.settings import LLM_MODEL_NAME


class OfferExtractionInput(BaseModel):
    offer_type: str
    offer: str


class OfferExtractor:
    llm: ChatOpenAI
    system_message_prompt: SystemMessage
    human_message_prompt_template: HumanMessagePromptTemplate
    total_cumulative_cost_of_usage: float
    temperature: float

    def __init__(
        self,
        model_name: str,
        system_message_prompt: str,
        human_message_prompt_template: str,
        temperature: float = 0.0,
    ) -> None:
        self.system_message_prompt = SystemMessage(content=system_message_prompt)
        self.human_message_prompt_template = HumanMessagePromptTemplate.from_template(
            human_message_prompt_template
        )
        self.llm = ChatOpenAI(model_name=model_name, temperature=temperature)
        self.chat_prompt = ChatPromptTemplate.from_messages(
            [self.system_message_prompt, self.human_message_prompt_template]
        )
        self.total_cumulative_cost_of_usage = 0.0

    def extract(self, offer_input: OfferExtractionInput) -> OfferSettings:
        with get_openai_callback() as cb:
            output: BaseMessage = self.llm.invoke(
                self.chat_prompt.format_prompt(
                    offer_type=offer_input.offer_type, offer=offer_input.offer
                ).to_messages()
            )

            self.update_cumulative_cost(cb.total_cost)

            extracted_offer: OfferSettings = OfferSettings(**json.loads(output.content))
            extracted_offer.full_offer = offer_input.offer
        return extracted_offer

    def update_cumulative_cost(self, extarction_cost: float) -> None:
        self.total_cumulative_cost_of_usage += extarction_cost


extractor: OfferExtractor = OfferExtractor(
    model_name=LLM_MODEL_NAME,
    system_message_prompt=system_message_string,
    human_message_prompt_template=human_message_prompt_template_string,
)


def extract_offer_info(
    offer: str, offer_type: str, offer_extractor: OfferExtractor = extractor
) -> OfferSettings:
    offer_input: OfferExtractionInput = OfferExtractionInput(
        offer=offer, offer_type=offer_type.split("_")[0]
    )

    return offer_extractor.extract(offer_input)
