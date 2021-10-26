from datetime import datetime

from db import db


class RegularTransferModel(db.Model):
    __tablename__ = 'regular_transfers'

    id = db.Column(db.Integer, primary_key=True)
    destination_card = db.Column(db.String)
    amount = db.Column(db.Integer)
    periodicity = db.Column(db.String)
    first_payment_date = db.Column(db.DateTime)
    account = db.relationship('AccountModel')
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))

    def __init__(self, destination_card, amount, periodicity, first_payment_date, account_id):
        self.date = datetime.now()
        self.destination_card = destination_card
        self.amount = amount
        self.periodicity = periodicity
        self.first_payment_date = first_payment_date
        self.account_id = account_id

    def json(self):
        return {
            'id': self.id,
            'destinationCard': self.destination_card,
            'amount': self.amount,
            'periodicity': self.periodicity,
            'firstPaymentDate': self.first_payment_date
        }

    @classmethod
    def get_by_id(cls, _id):
        return cls.query.find_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
