from .models import ClassifiedTransaction


def transactions_to_markdown(transactions: ClassifiedTransaction):
    transactions = list(reversed(transactions))
    markdown = list(map(transaction_to_markdown, transactions))
    return "\n".join(markdown)


def transaction_to_markdown(t: ClassifiedTransaction) -> str:
    return (
        f"| {t.vendor} | {t.amount} | {t.day} | {t.from_account} | Assets:Discover:Spent |\n"
        f"| {t.vendor} | {t.amount} | {t.day} "
        f"| Liabilities:CreditCard | Expenses:{t.from_account} |"
    )
