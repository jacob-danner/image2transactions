from openai import OpenAI
import json

from .utils import Transaction, RawTransaction, clean_response_content


def clean_raw_transactions(client: OpenAI, raw_transactions: list[RawTransaction]) -> list[Transaction]:
    response, content = None, None

    raw_transactions_str = json.dumps([rt.model_dump() for rt in raw_transactions])

    try:
        response = call_model(client, raw_transactions_str)
        content = json.loads(clean_response_content(response.choices[0].message.content))

        transactions = [Transaction(**t) for t in content]

        return transactions

    except Exception as e:
        print('Something went wrong. Logging state for debugging...')

        print(f'{response = }' if response else 'response DNE')
        print(f'{content = }' if response else 'response DNE')
        
        raise e


def call_model(client: OpenAI, raw_transactions_str: str):
    prompt = """
    You are an AI assistant that sanitzes transaction information for a downstream process.

    You are given an array of JSON objects with the following shape:

    {
        "vendor": "string",
        "amount": "string",
        "date": "string",
        "category": "string"
    }

    Your job is to clean the fields of each raw transaction in the following way:

    ---

    "vendor" = remove any junk characters that are uninformative about who the vendor is.
    this may include numbers or symbols, espeically _ or * or #
    remove any location information.
    infer more identifiable names when applicable.
    "vendor" examples: [
        "WALMART SC 01764 DES MOINES (WIA" => "WALMART",
        "AMZN MKTP US*L803414 AMZN.COM/BILLWAK951GIP" => "AMAZON",
        "CASESY'S #3932 URBANDALE IA" => "CASEY'S",
        "SQ BERNARDOS BURRITOS DES MOINES IA00000013592845" => "BERNARDO'S BURRITOS",
        "MCDONALDS 398 DES MOINES IAAPPLE PAY ENDING IN 9917" => "MCDONALD'S",
    ] 

    "amount" = remove the $ character so the amount can be parsed as a float downstream.
    "amount" examples: [
        "$28.72" => "28.72",
        "$19.18" => "19.18",
        "$104.99" => "104.99",
        "$16.04" => "16.04",
        "$4.52" => "4.52",
    ] 

    "date" = extract the day of the month from the date string. call it "day"
    "date" examples: [
        "Fri Jun 07, 2024" => "07",
        "Tue Jun 04, 2024" => "04",
        "Wed Jun 12, 2024" => "12",
        "Fri Jun 22, 2024" => "22",
        "Mon Jun 17, 2024" => "17",
    ] 

    "category" = fine the way it is.

    ---

    Following these instructions, each transaction will now be a cleaned JSON object of the shape:

    {
        "vendor": "string",
        "amount": "string",
        "day": "string",
        "category": "string"
    }

    Return all parsed transaction information as a JSON array of these objects
    such that it is directly parsable by pydantic.

    Please clean the transactions in this JSON.
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": raw_transactions_str
                    },
                ],
            }
        ],
    )

    return response