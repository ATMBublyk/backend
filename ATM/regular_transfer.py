import threading
import time

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from resources.transfer import Transfer
from models.transfer import TransferModel
from models.account import AccountModel


class RegularTransfer:
    def __init__(self, account_id: int, destination_card: str, amount: int, periodicity: str,
                 first_payment_date: datetime):
        self._account_id = account_id
        self._destination_card = destination_card
        self._amount = amount
        self._periodicity = periodicity
        self._first_payment_date = first_payment_date
        self.next_payment_date = first_payment_date
        self._account = AccountModel.get_by_id(account_id)
        # thread = threading.Thread(target=self.start)  # todo session
        # thread.start()
        self.start()

    def start(self):
        while True:
            current_date = datetime.now()
            if self.next_payment_date.date() == current_date.date():
                Transfer.make_transfer(self._account_id, self._destination_card, self._amount, True)
                if self._periodicity == 'everyday':
                    self.next_payment_date += timedelta(days=1)
                elif self._periodicity == 'weekly':
                    self.next_payment_date += timedelta(days=7)
                elif self._periodicity == 'monthly':
                    self.next_payment_date += relativedelta(months=1)
                elif self._periodicity == 'yearly':
                    self.next_payment_date += relativedelta(years=1)
                else:
                    raise Exception('incorrect periodicity')
            break
            # time.sleep(43200)
