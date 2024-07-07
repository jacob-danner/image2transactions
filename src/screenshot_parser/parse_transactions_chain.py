from ..models import RawTransaction
from ..resources import model

from langchain_core.runnables import RunnableLambda
from langchain_core.messages.human import HumanMessage
from langchain_core.output_parsers import StrOutputParser
import json
import base64


parse_prompt = """
__Task__: Parse transaction details from a credit card history image.

__Instructions__:
1. Parse each transaction as JSON in the following format:
{
    "vendor": "string",
    "amount": "string",
    "date": "string",
}
2. Each transaction may contain two numbers that look like "amount". Use the top one.
3. Return all parsed transaction information as a JSON array of these objects such that it
4. Output __only__ a JSON array of parsed transactions. Without any
additional text, symbols, or Markdown formatting.

__Desired output__: Example:
[
    {
        "vendor": "Vendor A",
        "amount": "100.00",
        "date": "2024-07-01",
    },
    {
        "vendor": "Vendor B",
        "amount": "200.00",
        "date": "2024-07-02",
    }
]
"""


def enocde_image(image_path: str):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# parse_transactions_chain = (image_path) => list[RawTransaction]

parse_transactions_chain = (
    RunnableLambda(
        lambda input_image: [
            HumanMessage(
                content=[
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{enocde_image(input_image)}",
                        },
                    },
                ]
            ),
            HumanMessage(parse_prompt),
        ]
    )
    | model
    | StrOutputParser()
    | RunnableLambda(
        lambda json_str: [RawTransaction(**t) for t in json.loads(json_str)]
    )
)
