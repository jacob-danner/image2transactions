from openai import OpenAI

from src.clean_transactions import clean_raw_transactions, Transaction
from src.utils import RawTransaction


client = OpenAI()

class TestImage1:
    raw_transactions = [
        RawTransaction(
            vendor="MCDONALD'S F33943 URBANDALE IA",
            amount="$6.61",
            date="Thu Jun 27, 2024",
            category="Restaurants"
        ),
        RawTransaction(
            vendor="WALMART STORE 01764 WINDSOR HEIGHIA",
            amount="$33.07",
            date="Thu Jun 27, 2024",
            category="Merchandise"
        ),
        RawTransaction(
            vendor="PANCHEROS 2122600895 IA",
            amount="$11.56",
            date="Wed Jun 26, 2024",
            category="Restaurants"
        ),
        RawTransaction(
            vendor="DOMINO'S 1720 DES MOINES IA",
            amount="$20.80",
            date="Tue Jun 25, 2024",
            category="Restaurants"
        ),
        RawTransaction(
            vendor="AMAZON PRIME*RC4F123U0 888-802-3080 WAYQAE3SP82RM",
            amount="$13.90",
            date="Mon Jun 24, 2024",
            category="Merchandise"
        )
    ]

    expected_transactions = [
        Transaction(vendor="MCDONALD'S", amount=6.61, day=27, category='Restaurants'),
        Transaction(vendor='WALMART', amount=33.07, day=27, category='Merchandise'),
        Transaction(vendor='PANCHEROS', amount=11.56, day=26, category='Restaurants'),
        Transaction(vendor="DOMINO'S", amount=20.8, day=25, category='Restaurants'),
        Transaction(vendor='AMAZON', amount=13.9, day=24, category='Merchandise')
    ]

    actual = clean_raw_transactions(client, raw_transactions)


    def test_image_1_actual_len(self):
        assert len(self.actual) == 5

    def test_image_1_actual_content(self):
        assert self.actual == self.expected_transactions