from datetime import datetime


class Withdrawal:
    count = 0

    def __init__(self, date: datetime, amount: int):
        self.count += 1
        self._id = self.count
        self._date = date
        self._amount = amount

    @property
    def id(self):
        return self._id

    @property
    def date(self):
        return self._date

    @property
    def amount(self):
        return self._amount
