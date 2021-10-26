from exceptions.exceptions import WrongPinException
from ATM.account import Account


class Bank:
    count = 0

    def __init__(self, name):
        self.count += 1
        self._id = self.count
        self.__accounts = {}  # card number, account
        self.bank_name = name

    def add_account(self, account: Account):
        self.__accounts[account.card_number] = account

    def get_account(self, card_number, pin):
        account = self.__accounts[card_number]
        if account.is_pin_right(pin):
            return account
        else:
            raise WrongPinException()
