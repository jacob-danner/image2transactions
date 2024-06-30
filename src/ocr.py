from openai import OpenAI
import base64
import json

from .utils import RawTransaction, clean_response_content


def image_to_raw_transactions(client: OpenAI, image_path: str) -> list[RawTransaction]:
    response, content = None, None

    encoded_image = enocde_image(image_path)

    try:
        response = call_model(client, encoded_image)
        content = json.loads(clean_response_content(response.choices[0].message.content))

        raw_transactions = [RawTransaction(**t) for t in content]

        return raw_transactions

    except Exception as e:
        print('Something went wrong. Logging state for debugging...')

        print(f'{response = }' if response else 'response DNE')
        print(f'{content = }' if response else 'response DNE')
        
        raise e


def enocde_image(image_path: str): 
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def call_model(client: OpenAI, encoded_image):
    prompt = """
    You are an AI assistant that parses transaction details from credit card history images.

    Parse each transaction as JSON in the following format:

    {
        "vendor": "string",
        "amount": "string",
        "date": "string",
        "category": "string"
    }

    Each transaction has 2 numbers that may like "amount", use the top one.

    Return all parsed transaction information as a JSON array of these objects
    such that it is directly parsable by pydantic.

    Please parse the transactions from this image, output __only__ the JSON array without any additional text.
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
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}",
                        },
                    },
                ],
            }
        ],
    )

    return response