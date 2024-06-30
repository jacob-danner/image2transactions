from src.format import transactions_to_markdown
from src.utils import Transaction


class TestImage1:
    transactions = [
        Transaction(vendor='WALMART', amount=33.07, day=27, category='Merchandise'),
        Transaction(vendor="MCDONALD'S", amount=6.61, day=27, category='Restaurants'),
        Transaction(vendor='PANCHEROS', amount=11.56, day=26, category='Restaurants'),
        Transaction(vendor="DOMINO'S", amount=20.8, day=25, category='Restaurants'),
        Transaction(vendor='AMAZON', amount=13.9, day=24, category='Merchandise'),
    ]

    expected_markdown = [
        "| AMAZON | 13.9 | 24 |",
        "| DOMINO'S | 20.8 | 25 |",
        "| PANCHEROS | 11.56 | 26 |",
        "| MCDONALD'S | 6.61 | 27 |",
        "| WALMART | 33.07 | 27 |",
    ]

    actual = transactions_to_markdown(transactions)


    def test_image_1_actual_len(self):
        assert len(self.actual) == 5

    def test_image_1_actual_content(self):
        assert self.actual == self.expected_markdown