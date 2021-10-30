from db import db


class AccountModel(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    pin = db.Column(db.String)
    card_number = db.Column(db.String)
    balance = db.Column(db.Float)
    surplus_card = db.Column(db.String)
    max_surplus_balance = db.Column(db.Integer)
    deposits = db.relationship('DepositModel', lazy='dynamic')
    withdrawals = db.relationship('WithdrawalModel', lazy='dynamic')
    transfers = db.relationship('TransferModel', lazy='dynamic')
    # regular_transfers = db.relationship('RegularTransferModel', lazy='dynamic')
    bank = db.relationship('BankModel')
    bank_id = db.Column(db.Integer, db.ForeignKey('banks.id'))

    def __init__(self, name, card_number, pin, bank_id, balance=0, surplus_card="", max_surplus_balance=0):
        self.name = name
        self.pin = pin
        self.card_number = card_number
        self.bank_id = bank_id
        self.balance = balance
        self.surplus_card = surplus_card
        self.max_surplus_balance = max_surplus_balance

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def get_balance(self):
        return self.balance

    def get_deposits(self):
        deposits = [deposit.json() for deposit in self.deposits.all()]
        return deposits

    def get_withdrawals(self):
        withdrawals = [withdrawal.json() for withdrawal in self.withdrawals.all()]
        return withdrawals

    def get_transfers(self):
        transfers = [transfer.json() for transfer in self.transfers.all()]
        return transfers

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
