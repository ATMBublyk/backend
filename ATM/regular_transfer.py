from datetime import datetime


class RegularTransfer:
    def __init__(self,  destination_card: str, amount: int, periodicity, first_payment_date: datetime):
        self._destination_card = destination_card
        self._amount = amount
        self._periodicity = periodicity
        self._first_payment_date = first_payment_date

    @property
    def destination_card(self):
        return self._destination_card

    @property
    def amount(self):
        return self._amount

    @property
    def periodicity(self):
        return self._periodicity

    @property
    def first_payment_date(self):
        return self._first_payment_date
