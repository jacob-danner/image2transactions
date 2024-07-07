from ..main import model
from ..models import ClassifiedTransaction, CleanedTransaction
from ..utils import Context

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

classify_template = """
__Task__: Classify the 'from_account' for the unclassified_transaction.

__Instructions__:
1. Analyze the provided classification_problem_context to infer the 'from_account' for the
unclassified_transaction.
2. Output the classified 'from_account'. __Don't guess.__ If there are no similar transactions to
infer from in classification_problem_context, return 'Discover:Main:UNKNOWN'.

__Desired output__: Be concise. Example:
'Discover:Main:Assets:Wants:Other'
---
{classification_problem_context}
---
"""

classify_prompt = ChatPromptTemplate.from_template(classify_template)


def create_classified_transaction(context: Context) -> ClassifiedTransaction:
    input_transaction: CleanedTransaction = context["input_transaction"]
    classification = context["classification"]
    return ClassifiedTransaction(
        **input_transaction.__dict__, from_account=classification
    )


# classify_chain = (
#   {"input_transaction": CleanedTransaction, "classification_problem_context": str}
# ) => {
#   "input_transaction": CleanedTransaction,
#   "classification_problem_context": str,
#   "classification": str
#   "classified_transaction": ClassifiedTransaction
# }

classify_chain = RunnablePassthrough.assign(
    classification=(classify_prompt | model | StrOutputParser())
) | RunnablePassthrough.assign(
    classified_transaction=(RunnableLambda(create_classified_transaction))
)
