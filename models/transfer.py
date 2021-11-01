from datetime import datetime

from db import db


class TransferModel(db.Model):
    __tablename__ = 'transfers'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    destination_card = db.Column(db.String)
    amount = db.Column(db.Float)
    account = db.relationship('AccountModel')
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))

    def __init__(self, date: datetime, destination_card, amount, account_id):
        self.date = date
        self.destination_card = destination_card
        self.amount = amount
        self.account_id = account_id

    def json(self):
        return {
            'id': self.id,
            'date': self.date.isoformat(),
            'destinationCard': self.destination_card,
            'amount': self.amount
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
