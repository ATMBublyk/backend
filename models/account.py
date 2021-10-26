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
    withdrawals = db.relationship('WithdrawalModel', lazy='dynamic')
    transfers = db.relationship('TransferModel', lazy='dynamic')
    regular_transfers = db.relationship('RegularTransferModel', lazy='dynamic')
    bank_id = db.Column(db.Integer, db.ForeignKey('banks.id'))
    bank = db.relationship('BankModel')

    def __init__(self, name, pin, card_number, bank_id, balance=0, surplus_card="", max_surplus_balance=0):
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

    @classmethod
    def get_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_balance_by_id(cls, _id):
        return cls.find_by_id(_id).balance
