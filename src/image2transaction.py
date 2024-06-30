from openai import OpenAI

from .ocr import image_to_raw_transactions
from .clean_transactions import clean_raw_transactions
from .format import transactions_to_markdown


def image2transaction(image_path: str) -> list[str]:
    client = OpenAI()
    raw_transactions = image_to_raw_transactions(client, image_path)
    transactions = clean_raw_transactions(client, raw_transactions)
    markdown_transactions = transactions_to_markdown(transactions)
    return markdown_transactions