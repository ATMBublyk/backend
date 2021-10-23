class ATM:
    def __init__(self):
        self._id = 0
        self._is_session: bool = False
        self._is_card_in: bool = False
        self._is_pin_right: bool = False
        self._bank = None

    def start_session(self, card_number, pin):
        pass

    def withdraw_money(self, amount):
        pass

    def get_balance(self) -> int:
        pass

    def put_money(self, amount):
        pass

    def transfer(self, amount, destination_card):
        pass

    def regular_transfer(self, amount, destination_card, periodicity, first_payment_date) -> int:
        pass

    def delete_regular_transfer(self, id):
        pass

    def end_session(self):
        pass
