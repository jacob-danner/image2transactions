from .parse_transactions_chain import parse_transactions_chain
from .clean_transactions_chain import clean_transactions_chain

# screenshot_parser_chain = (image_path) => list[CleanedTransaction]

screenshot_parser_chain = parse_transactions_chain | clean_transactions_chain
