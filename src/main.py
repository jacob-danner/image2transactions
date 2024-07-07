from .transaction_classifier.chains import transaction_classifier_chain
from .screenshot_parser.chains import screenshot_parser_chain
from .models import CleanedTransaction, ClassifiedTransaction
from .format_markdown import transactions_to_markdown


def run(image_path: str) -> None:
    cleaned_transactions: list[CleanedTransaction] = screenshot_parser_chain.invoke(
        image_path
    )
    print("cleaned_transactions:", cleaned_transactions, sep="\n")

    classified_transactions: list[ClassifiedTransaction] = [
        transaction_classifier_chain.invoke({"input_transaction": t})
        for t in cleaned_transactions
    ]
    print("classified_transactions:", classified_transactions, sep="\n")

    markdown = transactions_to_markdown(classified_transactions)
    print("markdown:", markdown, sep="\n")
