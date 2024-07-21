from langchain_core.prompts import ChatPromptTemplate

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

classify_template = """
__Task__: Classify the 'from_account' for the unclassified_transaction.

__Instructions__:
1. Analyze the provided classification_problem_context to infer the 'from_account' for the
unclassified_transaction.
2. Output the classified 'from_account'. __Don't guess.__ If there are no similar transactions to
infer from in classification_problem_context, return Assets:Discover:Main:UNKNOWN.

__Possible accounts__:
- Assets:Discover:Main:Wants:Other
- Assets:Discover:Main:Wants:Monthly
- Assets:Discover:Main:Needs:Gas
- Assets:Discover:Main:Needs:Groceries
- Assets:Discover:Main:Needs:Monthly
- Assets:Discover:Main:Needs:Monthly

__Desired output__: Be concise. Example:
Assets:Discover:Main:Wants:Other
---
{classification_problem_context}
---
"""

classify_prompt = ChatPromptTemplate.from_template(classify_template)
