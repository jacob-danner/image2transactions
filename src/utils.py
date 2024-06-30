from pydantic import BaseModel


class RawTransaction(BaseModel):
    vendor: str
    amount: str
    date: str
    category: str


class Transaction(BaseModel):
    vendor: str
    amount: float
    day: int
    category: str


# ---

def clean_response_content(content: str):
    content = content.removeprefix('```json\n')
    content = content.removesuffix('```')
    return content