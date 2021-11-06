from datetime import datetime

from db import db


class TransferModel(db.Model):
    __tablename__ = 'transfers'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    destination_card = db.Column(db.String)
    amount = db.Column(db.Float)
    is_regular = db.Column(db.Boolean)
    is_auto = db.Column(db.Boolean)
    account = db.relationship('AccountModel')
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))

    def __init__(self, date: datetime, destination_card, amount, account_id, is_regular: bool, is_auto: bool):
        self.date = date
        self.destination_card = destination_card
        self.amount = amount
        self.account_id = account_id
        self.is_regular = is_regular
        self.is_auto = is_auto

    def json(self):
        return {
            'id': self.id,
            'date': self.date.isoformat(),
            'destinationCard': self.destination_card,
            'amount': self.amount,
            'isRegular': self.is_regular,
            'isAuto': self.is_auto
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
