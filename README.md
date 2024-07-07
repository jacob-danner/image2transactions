## Steps

1. Parse Credit Card History Image
    - Parse the transactions from screenshot of credit card transactions into JSON (model)
    - Edit / clean fields of the JSON transactions as desired
2. RAG
    - For each parsed transaction:
        - Query opensearch on transaction name. Collect n documents
        - Classify the transaction's 'from' account (model), given the n documents in context
3. Format in desired markdown format
