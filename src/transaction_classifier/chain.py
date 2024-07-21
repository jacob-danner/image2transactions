from .prompts import rank_prompt, classify_prompt

from ..utils import Context
from ..models import CleanedTransaction, ClassifiedTransaction
from ..resources import model, retriever

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.documents import Document

# ---


def retrieve_transactions(context: Context) -> list[Document]:
    input_transaction_vendor = context["input_transaction"].vendor
    return retriever.invoke(input_transaction_vendor)


def format_context(docs: list[Document]):
    return "\n".join([d.page_content for d in docs])


def stringify_input_transaction(context: Context) -> str:
    input_transaction = context["input_transaction"]
    return input_transaction.model_dump_json()


# ---


def create_classified_transaction(context: Context) -> ClassifiedTransaction:
    input_transaction: CleanedTransaction = context["input_transaction"]
    classification = context["classification"]
    return ClassifiedTransaction(
        **input_transaction.__dict__, from_account=classification
    )


# transaction_classifier_chain = (
#   {"input_transaction": CleanedTransaction}
# ) => {
#   "input_transaction": CleanedTransaction,
#   "classification_problem_context": str,
#   "classification": str
#   "classified_transaction": ClassifiedTransaction
# }

transaction_classifier_chain = (
    RunnablePassthrough.assign(
        classification_problem_context={
            "retrieved_transactions": RunnableLambda(retrieve_transactions)
            | format_context,
            "unclassified_transaction": RunnableLambda(stringify_input_transaction),
        }
        | rank_prompt
        | model
        | StrOutputParser()
    )
    | RunnablePassthrough.assign(
        classification=(classify_prompt | model | StrOutputParser())
    )
    | RunnablePassthrough.assign(
        classified_transaction=(RunnableLambda(create_classified_transaction))
    )
)
