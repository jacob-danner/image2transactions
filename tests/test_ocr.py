import pytest
from openai import OpenAI

from src.ocr import image_to_raw_transactions
from src.utils import RawTransaction


client = OpenAI()

class TestImage1:
    expected_raw_transactions = [
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

    actual = image_to_raw_transactions(client, 'tests/images/1.png')


    def test_image_1_actual_len(self):
        assert len(self.actual) == 5

    def test_image_1_actual_content(self):
        assert self.actual == self.expected_raw_transactions