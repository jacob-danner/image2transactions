from .utils import format_context, stringify_transaction, runnable_log_to_file

from ..opensearch.client import client, index_name
from ..opensearch.retrieve import OpenSearchRetriever

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough


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

classify_template = """
__Task__: Classify the 'from_account' for the unclassified_transaction.

__Instructions__:
1. Analyze the provided classification_problem_context to infer the 'from_account' for the unclassified_transaction.
2. Output the classified 'from_account'.
   - __Don't guess.__ If there are no similar transactions to infer from in 'classification_problem_context', return 'Discover:Main:UNKNOWN'.

__Desired output__: Be concise. Example:
'Discover:Main:Assets:X'
---
{classification_problem_context}
---
"""

rank_prompt = ChatPromptTemplate.from_template(rank_template)
classify_prompt = ChatPromptTemplate.from_template(classify_template)

model = ChatOpenAI(model='gpt-4o')
retriever = OpenSearchRetriever(client=client, index_name=index_name)

rank_chain = (
    RunnableLambda(lambda transaction: runnable_log_to_file('## Rank Chain Start', to_return=transaction)) 
    | {"retrieved_transactions": RunnableLambda(lambda t: retriever.invoke(t.vendor)) | format_context,
       "unclassified_transaction": RunnableLambda(stringify_transaction)}
    | rank_prompt 
    | RunnableLambda(lambda prompt_value: runnable_log_to_file('### Rank Chain Prompt', to_return=prompt_value, content=prompt_value.to_string()))
    | model
    | StrOutputParser()
    | RunnableLambda(lambda model_output: runnable_log_to_file('### Rank Chain Model Output', to_return=model_output, content=model_output))
)

classify_chain = (
    RunnableLambda(lambda transaction: runnable_log_to_file('## Classify Chain Start', to_return=transaction)) 
    | {"classification_problem_context": RunnablePassthrough()}
    | classify_prompt
    | RunnableLambda(lambda prompt_value: runnable_log_to_file('### Classify Chain Prompt', to_return=prompt_value, content=prompt_value.to_string()))
    | model
    | StrOutputParser()
    | RunnableLambda(lambda model_output: runnable_log_to_file('### Classify Chain Model Output', to_return=model_output, content=model_output))
)

transaction_classifier_chain = (
    RunnableLambda(lambda transaction: runnable_log_to_file('# TRANSACTION CLASSIFIER CHAIN START', to_return=transaction))
    | rank_chain
    | classify_chain
    | RunnableLambda(lambda classification: runnable_log_to_file('#-----#', to_return=classification))
)
