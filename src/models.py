from pydantic import BaseModel


class RawTransaction(BaseModel):
    vendor: str
    amount: str
    date: str


class CleanedTransaction(BaseModel):
    vendor: str
    amount: float
    day: int


class ClassifiedTransaction(BaseModel):
    vendor: str
    amount: float
    day: int
    from_account: str
