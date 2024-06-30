from .utils import Transaction


def transactions_to_markdown(transactions: Transaction):
    transactions = list(reversed(transactions))
    markdown = list(map(transaction_to_markdown, transactions))
    return markdown


def transaction_to_markdown(t: Transaction) -> str:
    return f'| {t.vendor} | {t.amount} | {t.day} |'