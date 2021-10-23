class Account:
    count = 0

    def __init__(self, name, pin, card_number, balance, card_type):
        self.count += 1
        self.__id = self.count
        self.__name = ''
        self.__pin = ''
        self.__card_number = ''
        self.__balance = 0
        self.__card_type = None
        self.__regular_transfers = []
        self.__transfers = []
        self.__withdrawals = []

    @property
    def name(self):
        return self.__name

    def is_pin_right(self, pin: str):
        return self.__pin == pin

    @property
    def card_number(self):
        return self.__card_number

    @property
    def balance(self):
        return self.__balance

    @property
    def card_type(self):
        return self.card_type

    @property
    def regular_transfer(self):
        return self.__regular_transfers

    @property
    def transfers(self):
        return self.__transfers

    @property
    def withdrawals(self):
        return self.__withdrawals

