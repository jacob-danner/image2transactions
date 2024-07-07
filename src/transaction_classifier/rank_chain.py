from ..resources import model, retriever
from ..utils import Context

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.documents import Document

rank_template = """
__Task__: Rank the provided transactions based on their similarity to the unclassified_transaction.

__Instructions__:
1. Rank transactions:
    - Assign a weighted score of 0-10 for each criterion.
    - Weights: Vendor: 50%, Amount: 30%, Day: 20%
2. Output:
    - Ranked transactions by similarity.
    - __NOTE__: If there are no provided transactions to rank, then leave ranked_by_similarity empty

__Desired output__: Be concise. Example:
    ranked_by_similarity:
        - transaction: <transaction1>
            score: <score>
        - transaction: <transaction2>
            score: <score>
        ...
        - transaction: <transactionN>
            score: <score>
    unclassified_transaction: <unclassified_transaction>
---
{retrieved_transactions}
---
unclassified_transaction: {unclassified_transaction}
"""

rank_prompt = ChatPromptTemplate.from_template(rank_template)


def retrieve_transactions(context: Context) -> list[Document]:
    input_transaction_vendor = context["input_transaction"].vendor
    return retriever.invoke(input_transaction_vendor)


def format_context(docs: list[Document]):
    return "\n".join([d.page_content for d in docs])


def stringify_transaction(context: Context) -> str:
    input_transaction = context["input_transaction"]
    return input_transaction.model_dump_json()


# rank_chain = (
#   {"input_transaction": CleanedTransaction}
# ) => {
#   "input_transaction": CleanedTransaction,
#   "classification_problem_context": str
# }

rank_chain = RunnablePassthrough.assign(  # add classification to the result
    classification_problem_context={
        "retrieved_transactions": RunnableLambda(retrieve_transactions)
        | format_context,
        "unclassified_transaction": RunnableLambda(stringify_transaction),
    }
    | rank_prompt
    | model
    | StrOutputParser()
)
