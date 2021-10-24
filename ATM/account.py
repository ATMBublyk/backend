from typing import Final


class Account:
    count = 0

    def __init__(self, name, pin, card_number):
        self.count += 1
        self._id: Final = self.count
        self._name = name
        self._pin = pin
        self._card_number = card_number
        self._balance = 0
        self._regular_transfers = []
        self._transfers = []
        self._withdrawals = []
        self._surplus_card = ""
        self._max_surplus_balance = 0

    def deposit(self, amount: int):
        self._balance += amount

    def withdraw(self, amount: int):
        self._balance -= amount

    def add_surplus_card(self, card_number: str):
        self._surplus_card = card_number

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

    def is_pin_right(self, pin: str):
        return self._pin == pin

    @property
    def balance(self):
        return self._balance

    @property
    def regular_transfer(self):
        return self._regular_transfers

    @property
    def card_number(self):
        return self._card_number

    @property
    def transfers(self):
        return self._transfers

    @property
    def withdrawals_history(self):
        return self._withdrawals

