## Steps

1. Parse Credit Card History Image
    - Parse the transactions from screenshot of credit card transactions into JSON (model)
    - Edit / clean fields of the JSON transactions as desired
2. RAG
    - For each parsed transaction:
        - Query opensearch on transaction name. Collect n documents
        - Classify the transaction's 'from' account (model), given the n documents in context
3. Format in desired markdown format

## TODO

- [x] dataset
    - [x] extract transactions data into desired form
    - [x] upload data opensearch










---

- [ ] Save each run's data to file
- [ ] Testing
    - [ ] Use an LLM to brainstorm assertions
    - [ ] Implement statistical testing. How often does it give me what I want?
- [ ] Read about EvalGen
- [ ] Use the messages api to use "system", "user", and "assistant" roles to put words in the model's mouth. This might enable better n shot prompting with back and forth examples as opposed to just a user prompt.
- [ ] Extract token info (input and output) from response. Calculate cost models from this information

(On the instructor branch)
- [ ] Read this [blog](https://hamel.dev/blog/posts/prompt/) to figure out what instructor is actually prompting
