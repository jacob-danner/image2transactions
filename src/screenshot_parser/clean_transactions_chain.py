from ..resources import model
from ..models import CleanedTransaction

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
import json

clean_template = """
__Task__: Clean transaction information for a downstream process.

__Instructions__:
1. You are given an array of JSON objects with the following shape:
    {{
        "vendor": "string",
        "amount": "string",
        "date": "string",
    }}
2. Clean the fields of each raw transaction in the following way:
    - "vendor": Remove any junk characters that are uninformative about who the vendor is. This may
      include numbers or symbols, especially _ or *.
      Remove any location information. Infer more identifiable names when applicable.
        - Examples:
            - "WALMART SC 01764 DES MOINES (WIA" => "WALMART"
            - "AMZN MKTP US*L803414 AMZN.COM/BILLWAK951GIP" => "AMAZON"
            - "CASESY'S #3932 URBANDALE IA" => "CASEY'S"
            - "SQ BERNARDOS BURRITOS DES MOINES IA00000013592845" => "BERNARDO'S BURRITOS"
            - "MCDONALDS 398 DES MOINES IAAPPLE PAY ENDING IN 9917" => "MCDONALD'S"
    - "amount": Remove the $ character so the amount can be parsed as a float downstream.
        - Examples:
            - "$28.72" => "28.72"
            - "$19.18" => "19.18"
            - "$104.99" => "104.99"
            - "$16.04" => "16.04"
            - "$4.52" => "4.52"
    - "date": Extract the day of the month from the date string and call it "day".
        - Examples:
            - "Fri Jun 07, 2024" => "07"
            - "Tue Jun 04, 2024" => "04"
            - "Wed Jun 12, 2024" => "12"
            - "Fri Jun 22, 2024" => "22"
            - "Mon Jun 17, 2024" => "17"

3. Return all cleaned transaction information as a JSON array of these objects such that it 
is directly parsable by pydantic.
4. Output __only__ the JSON array without any additional text, symbols, or Markdown formatting.

__Desired output__: Example:
[
    {{
        "vendor": "WALMART",
        "amount": "28.72",
        "day": "07",
    }},
    {{
        "vendor": "AMAZON",
        "amount": "19.18",
        "day": "04",
    }}
]

Please clean the transactions in this JSON.
---
{transactions_json}
"""

# clean_transaction_chain = (list[RawTransaction]) => list[CleanTransaction]

clean_prompt = ChatPromptTemplate.from_template(clean_template)

clean_transactions_chain = (
    {
        "transactions_json": RunnableLambda(
            lambda raw_transactions: json.dumps(
                [rt.model_dump() for rt in raw_transactions]
            )
        ),
    }
    | clean_prompt
    | model
    | StrOutputParser()
    | RunnableLambda(
        lambda json_str: [CleanedTransaction(**t) for t in json.loads(json_str)]
    )
)
