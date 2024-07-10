from .rank_chain import rank_chain
from .classify_chain import classify_chain
from ..utils import Context
from ..models import ClassifiedTransaction

from langchain_core.runnables import RunnableLambda


def get_classified_transaction(context: Context) -> ClassifiedTransaction:
    return context["classified_transaction"]


# transaction_classifier_chain = (
#   {"input_transaction": CleanedTransaction}
# ) => ClassifiedTransaction

transaction_classifier_chain = (
    rank_chain | classify_chain | RunnableLambda(get_classified_transaction)
)
