from datetime import datetime

from db import db


class DepositModel(db.Model):
    __tablename__ = 'deposits'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    amount = db.Column(db.Float)
    account = db.relationship('AccountModel')
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))

    def __init__(self, date: datetime, amount: float, account_id: int):
        self.date = date
        self.amount = amount
        self.account_id = account_id

    def json(self):
        return {
            "id": self.id,
            "date": self.date.isoformat(),
            "amount": self.amount
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
