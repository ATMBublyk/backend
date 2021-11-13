from db import db


class AccountModel(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    pin = db.Column(db.String)
    card_number = db.Column(db.String)
    balance = db.Column(db.Float)
    deposits = db.relationship('DepositModel', lazy='dynamic')
    withdrawals = db.relationship('WithdrawalModel', lazy='dynamic')
    transfers = db.relationship('TransferModel', lazy='dynamic')
    regular_transfers = db.relationship('RegularTransferModel', lazy='dynamic')
    bank_id = db.Column(db.Integer, db.ForeignKey('banks.id'))

    # surpluses-account
    surpluses_destination_card = db.Column(db.String)
    surpluses_max_balance = db.Column(db.Float)
    have_surpluses_account = db.Column(db.Boolean)

    def __init__(self, name, card_number, pin, bank_id, balance=0, surpluses_destination_card="",
                 surpluses_max_balance=0, have_surpluses_account=False):
        self.name = name
        self.pin = pin
        self.card_number = card_number
        self.bank_id = bank_id
        self.balance = balance
        self.surpluses_destination_card = surpluses_destination_card
        self.surpluses_max_balance = surpluses_max_balance
        self.have_surpluses_account = have_surpluses_account

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def get_balance(self):
        return self.balance

    def get_deposits(self):
        deposits = [deposit.json() for deposit in self.deposits.all()]
        deposits_dict = {"deposits": deposits}
        return deposits_dict

    def get_withdrawals(self):
        withdrawals = [withdrawal.json() for withdrawal in self.withdrawals.all()]
        withdrawals_dict = {"withdrawals": withdrawals}
        return withdrawals_dict

    def get_transfers(self):
        transfers = [transfer.json() for transfer in self.transfers.all()]
        transfers_dict = {"transfers": transfers}
        return transfers_dict

    def get_regular_transfer_by_id(self, _id):
        for regular_transfer in self.regular_transfers.all():
            if regular_transfer.id == _id:
                return regular_transfer

    def get_regular_transfers(self):
        regular_transfers = [regular_transfer.json() for regular_transfer in self.regular_transfers.all()]
        regular_transfers_dict = {"regularTransfers": regular_transfers}
        return regular_transfers_dict

    def json(self):
        return {
            "name": self.name,
            "cardNumber": self.card_number,
            "balance": self.balance,
            "bankId": self.bank_id
        }

    def json_admin(self):
        return {
            "id": self.id,
            "name": self.name,
            "cardNumber": self.card_number,
            "balance": self.balance,
            "bankId": self.bank_id,
            "pin": self.pin
        }

    @classmethod
    def is_card_valid(cls, card_number):
        return cls.query.filter_by(card_number=card_number).first() is not None

    @classmethod
    def get_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_bank_id(cls, card_number):
        account = cls.query.filter_by(card_number=card_number).first()
        return account.bank_id

    @classmethod
    def get_by_card(cls, card_number):
        return cls.query.filter_by(card_number=card_number).first()
