from datetime import datetime


class Transfer:
    count = 0

    def __init__(self, sender_card: str, destination_card: str, amount: int):
        self.count += 1
        self._id: int = self.count
        self._date = datetime.now()
        self._destination_card = destination_card
        self._sender_card = sender_card
        self._amount = amount

    @property
    def id(self):
        return self._id

