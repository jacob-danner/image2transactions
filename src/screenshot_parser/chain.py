from .prompts import parse_template, clean_prompt
from ..utils import Context


from ..models import RawTransaction, CleanedTransaction
from ..resources import model

from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.messages.human import HumanMessage
from langchain_core.output_parsers import StrOutputParser
import json
import base64


def enocde_image(image_path: str):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def build_parse_messages(context: Context) -> list[HumanMessage]:
    encoded_image = enocde_image(context["image_path"])
    messages = [
        HumanMessage(
            content=[
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_image}",
                    },
                },
            ]
        ),
        HumanMessage(parse_template),
    ]

    return messages


# ---


def create_raw_transactions(json_str: str) -> list[RawTransaction]:
    return [RawTransaction(**t) for t in json.loads(json_str)]


def create_raw_transactions_json_str(context: Context) -> str:
    raw_transactions = context["raw_transactions"]
    return json.dumps([rt.model_dump() for rt in raw_transactions])


# ---


def create_clean_transactions(json_str: str) -> list[CleanedTransaction]:
    return [CleanedTransaction(**t) for t in json.loads(json_str)]


# screenshot_parser_chain = (
#   {"image_path": str}
# ) => {
#   "image_path": str
#   "raw_transactions": list[RawTransaction],
#   "raw_transactions_json_str": str,
#   "cleaned_transactions": list[CleanedTransaction]
# }


screenshot_parser_chain = (
    RunnablePassthrough.assign(
        raw_transactions=RunnableLambda(build_parse_messages)
        | model
        | StrOutputParser()
        | RunnableLambda(create_raw_transactions)
    )
    | RunnablePassthrough.assign(
        raw_transactions_json_str=RunnableLambda(create_raw_transactions_json_str)
    )
    | RunnablePassthrough.assign(
        cleaned_transactions=clean_prompt
        | model
        | StrOutputParser()
        | RunnableLambda(create_clean_transactions)
    )
)
