## The motive:

I budget my money / track my expenses inside plain text files via a tool called hledger. This tool requires that each transaction is formatted in a particular way - vendor/transaction name, amount, day, and the name of the accounts the money came from and goes to.
This works great for me, but it means that few weeks I have to sit down and manually enter each transaction. This is tedious, time consuming, and error prone. I'd like to be able to avoid this manual data entry.

## The solution:

### The general flow of the app

- screenshot parser
	- input screenshot of credit card transactions
	- parse each transaction into a `RawTransaction` (vendor, amount, day) via llm
	- convert each `RawTransaction` into a `CleanedTransaction` (remove store id, location, and other junk from vendor) via llm
	- return a list of `CleanedTransactions`
- classification (per `CleanedTransaction`)
	- search db for previous transactions
        - rank the retrieved previous transactions in order of how similar they are to the `CleanedTransaction` via llm and add to context
	- given the context, classify the transaction's from_account (exists in the db transactions, but not on the `CleanedTransaction`) via llm
	- return a `ClassifiedTransaction` (vendor, amount, day, from_account)
- format
	- print each `ClassifiedTransaction` in the required format