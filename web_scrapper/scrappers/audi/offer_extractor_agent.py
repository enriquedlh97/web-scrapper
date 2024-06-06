import json
from typing import Final

from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate)
from langchain.schema import BaseMessage, SystemMessage
from langchain_community.callbacks import get_openai_callback
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from web_scrapper.scrappers.audi.models_library import OfferSettings

LLM_MODEL_NAME: str = "gpt-3.5-turbo-0125"

system_message_string: Final[
    str
] = """
You are an expert system specializing in extracting information from
offers of vehicles like the ones found in websites for car
dealerships. You specialize in offers for Audi.

You work mainly with in 2 types of offers, although others are allowed:
1. Financial Offer.
2. Promotion Offer.

You are given as input 2 things:
1. The type of offer: `Financial Offer` or `Promotion Offer`.
2. The text describing the offer.

From the text, you have to extract the following information:
```information to extract
payment: float | null
payment_label: str | null
term: int | null
down_payment: float | null
down_payment_label: str | null
expiration: str (YYYY-MM-DD)
price: str | null
disclaimer: str
apr: str | null
name: str | null
amount: float | null
msrp: float | null
```

The offers may contain only some information, you are supposed to:
1. Read the offer very carefully.
2. Identified the fields that can be found in the offer.
3. Extract the information
3. Write the extracted information formatted as a json.


Here you can find a description of what each field means. Use these
definitions to look for the information in the offer.

```definitions
payment: (float | null) It refers to the monetary amount to be payed
    indicated by the offer. If the offer includes it, it will always be
    a numeric value, for example '949.99'.
payment_label: (str | null) Refers how often the 'payment' (previous field)
    has to be made, it is usually in months (eg, 'Monthly payment') but can
    be define in other periods like days, weeks, years, etc.
term: (int | null) It refers to the number of payments (see previous 2 fields)
    to be made. For example it the offer indicates a monthly payment of $949.99
    for 12 months, then the term is '12' because it refers to the 12 months.
down_payment: (float | null) The initial payment indicated by the offer.
down_payment_label: (str | null) It gives additional information about the
    terms of the down payment. For example, if the offer says "A down payment
    of $9,829 due from customer at lease signing", then the
    'down_payment_label' would be "due from customer at lease signing".
expiration: (date) The date in which the offer expires. You should always write
    it following the ISO 8601 format for dates, which is 'YYYY-MM-DD'. For
    example, for 'Jun 04, 2024' you have to write '2024-06-04'.
price: (str | null) Some offers give a special price, this refers to that
    special price mentioned in the offer. If it is included, then it is always
    a monetary value.
disclaimer: (str) The textual description provided as disclaimer, it is usually
    indicated by the word "Disclaimer".
apr: (str | null) The Annual Percentage Rate mentioned in the offer.
name: (str | null) A brief name describing the offer. If it is not included,
    you can come up with one. If you come up with one make sure you provide a
    very brief, concise, and descriptive name for the offer.
amount: (float | null) Some offers give a bonus or some type of monetary
    reward. The 'amount' refers to that value. If it is included it is always
    a numeric value.
msrp: (float | null) Refers to the the manufacturer's suggested retail price.
    If it is included, it is always a numeric value.
```


Remember that not all offers will have information for all the fields. If
you cannot find information for a specific field you have to set it to null.
Only add the information to the corresponding field when you are completely
sure it is mentioned in the offer.

Now I will give you some examples of offers and what the expected output
has to look like.

IMPORTANT: Please write the result as json

Example 1. The following is a 'Financial Offer'
```Example financial offer
3.99% APR* For 60 Months.\nManufacturer Offers\n3.99% APR for 60 months\nOffer only valid Jun 04, 2024 through Jul 01, 2024\n3.99% APR* for 60 months. For highly qualified customers.   See Trims\nDisclaimer(s) :\n*3.99% APR, no down payment required, available on new, unused 2024 Audi A3 and S3 models financed by Audi Financial Services through participating dealers. Example: 3.99% APR, monthly payment for every $1,000 you finance for 60 months is $18.41. Not all customers will qualify for credit approval or advertised APR. Offer ends July 1, 2024. Subject to credit approval by Audi Financial Services. Offer not valid in Puerto Rico. See your Audi dealer for details or, for general product information, call 1.800.FOR.AUDI (367.2834). © 2024 Audi of America, Inc.\nRequest More Info\nView Inventory
```

Below, delimited by triple backticks, is the expected output for the
'Financial Offer'. Be sure to always follow the format and never write your
output if it is not formatted as below:
```
{
  "payment": null,
  "payment_label": null,
  "term": 60,
  "down_payment": 0.0,
  "down_payment_label": "No down payment required",
  "expiration": "2024-07-01",
  "price": null,
  "disclaimer": "Disclaimer(s) :\n*3.99% APR, no down payment required, available on new, unused 2024 Audi A3 and S3 models financed by Audi Financial Services through participating dealers. Example: 3.99% APR, monthly payment for every $1,000 you finance for 60 months is $18.41. Not all customers will qualify for credit approval or advertised APR. Offer ends July 1, 2024. Subject to credit approval by Audi Financial Services. Offer not valid in Puerto Rico. See your Audi dealer for details or, for general product information, call 1.800.FOR.AUDI (367.2834). © 2024 Audi of America, Inc.",
  "apr": "3.99%",
  "name": "3.99% APR* For 60 Months | Manufacturer Offers",
  "amount": null,
  "msrp": null
}

```


Example 2. The following is a 'Promotion Offer'
```Example promotion offer
$2,000 National Audi Credit*\nManufacturer Offers\nOffer only valid Jun 04, 2024 through Jul 01, 2024\nReceive a $2,000 customer bonus when you purchase or lease a select, new 2024 Audi A3. Cannot be combined with Special APR or lease rates*   See Trims\nDisclaimer(s) :\n*Bonus cannot be combined with discounted Audi Financial Services Special Lease or Special APR Programs, or on Fleet or Dealership Sale Program vehicles. Audi of America, Inc. will pay a $2,000 customer bonus when you purchase a new, unused 2024 Audi A3 through participating dealers from June 4, 2024 to July 1, 2024. Customer bonus applied toward MSRP and is not available for cash. May not be combined Puerto Rico Assistance Program. Offer not valid in Puerto Rico. See your local Audi dealer or, for general product information, call 1-800-FOR-AUDI. © 2024 Audi of America, Inc.\nRequest More Info\nView Inventory
```

Below, delimited by triple backticks, is the expected output for the
'Promotion Offer'. Be sure to always follow the format and never write your
output if it is not formatted as below:
```
{
  "payment": null,
  "payment_label": null,
  "term": null,
  "down_payment": null,
  "down_payment_label": null,
  "expiration": "2024-07-01",
  "price": null,
  "disclaimer": "Disclaimer(s) :\n*Bonus cannot be combined with discounted Audi Financial Services Special Lease or Special APR Programs, or on Fleet or Dealership Sale Program vehicles. Audi of America, Inc. will pay a $2,000 customer bonus when you purchase a new, unused 2024 Audi A3 through participating dealers from June 4, 2024 to July 1, 2024. Customer bonus applied toward MSRP and is not available for cash. May not be combined Puerto Rico Assistance Program. Offer not valid in Puerto Rico. See your local Audi dealer or, for general product information, call 1-800-FOR-AUDI. © 2024 Audi of America, Inc.",
  "apr": null,
  "name": "$2,000 National Audi Credit* | Manufacturer Offers",
  "amount": 2000.0,
  "msrp": null
}

```

IMPORTANT: Remember to only write the result as json and do not provide any
explanation, just write the expected json with the corresponding information.

Do not include triple backticks in your answer, just write the plain json string.

Make sure you always follow the output format, because your output will be read
with python using: 'json.loads()'.
"""

human_message_prompt_template_string: Final[
    str
] = """
Below, delimited by triple backticks, you will find the offer.

This is a {offer_type} offer. Please extract the information from the offer
and write the output in the appropriate format.

```
{offer}
```
"""


class OfferExtractionInput(BaseModel):
    offer_type: str
    offer: str


class OfferExtractor:
    llm: ChatOpenAI
    system_message_prompt: SystemMessage
    human_message_prompt_template: HumanMessagePromptTemplate
    max_token_limit: int
    total_cumulative_cost_of_usage: float
    completion_tokens: int
    decision_llm: ChatOpenAI | None
    decision_system_message_prompt: SystemMessage
    decision_human_message_prompt_template: HumanMessagePromptTemplate

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


def extract_offer_info(offer: str, offer_type: str) -> OfferSettings:
    offer_input: OfferExtractionInput = OfferExtractionInput(
        offer=offer, offer_type=offer_type.split("_")[0]
    )
    offer_extarctor: OfferExtractor = OfferExtractor(
        model_name=LLM_MODEL_NAME,
        system_message_prompt=system_message_string,
        human_message_prompt_template=human_message_prompt_template_string,
    )

    return offer_extarctor.extract(offer_input)
