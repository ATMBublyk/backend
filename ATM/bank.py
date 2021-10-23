from exceptions.exceptions import WrongPinException


class Bank:
    def __init__(self, name):
        self.__accounts = {}  # card number, account
        self.bank_name = name

    def add_account(self, account):
        self.__accounts[account.card_number] = account

    def get_account(self, card_number, pin):
        account = self.__accounts[card_number]
        if account.is_pin_right(pin):
            return account
        else:
            raise WrongPinException()
