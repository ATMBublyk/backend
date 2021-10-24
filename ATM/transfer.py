from datetime import datetime


class Transfer:
    count = 0

    def __init__(self, destination_card: str, amount: int):
        self.count += 1
        self._id: int = self.count
        self._date = datetime.now()
        self._destination_card = destination_card
        self._amount = amount

    @property
    def id(self):
        return self._id

    @property
    def date(self):
        return self._date

    @property
    def destination_card(self):
        return self.destination_card

    @property
    def amount(self):
        return self._amount
