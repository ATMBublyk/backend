class Account:
    def __init__(self):
        self._id = 0
        self._name = ''
        self._pin = ''
        self._card_number = ''
        self._budget = 0
        self._card_type = None
        self._regular_payments = []
        self._transfers = []
        self._withdrawals = []
