from datetime import datetime

from transfer import Transfer


class RegularTransfer(Transfer):
    def __init__(self, sender_card: str, destination_card: str, amount: int, periodicity, first_payment_date: datetime):
        super().__init__(sender_card, destination_card, amount)
        self.__periodicity = periodicity
        self.__first_payment_date = first_payment_date


