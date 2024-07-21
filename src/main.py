from .transaction_classifier.chain import transaction_classifier_chain
from .screenshot_parser.chain import screenshot_parser_chain
from .format_markdown import transactions_to_markdown
from .models import ClassifiedTransaction
from .utils import Context


def run(image_path: str) -> str:
    # screenshot_parser_chain = (
    #   {"image_path": str}
    # ) => {
    #   "image_path": str
    #   "raw_transactions": list[RawTransaction],
    #   "raw_transactions_json_str": str,
    #   "cleaned_transactions": list[CleanedTransaction]
    # }
    cleaned_transactions: Context = screenshot_parser_chain.invoke(
        {"image_path": image_path}
    )["cleaned_transactions"]

    # transaction_classifier_chain = (
    #   {"input_transaction": CleanedTransaction}
    # ) => {
    #   "input_transaction": CleanedTransaction,
    #   "classification_problem_context": str,
    #   "classification": str
    #   "classified_transaction": ClassifiedTransaction
    # }
    classified_transactions: list[ClassifiedTransaction] = [
        transaction_classifier_chain.invoke({"input_transaction": t})["classified_transaction"]
        for t in cleaned_transactions
    ]

    markdown = transactions_to_markdown(classified_transactions)
    return markdown
