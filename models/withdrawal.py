from datetime import datetime

from db import db


class WithdrawalModel(db.Model):
    __tablename__ = 'withdrawals'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    amount = db.Column(db.Integer)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    account = db.relationship('AccountModel')

    def __init__(self, amount, account_id):
        self.date = datetime.now()
        self.amount = amount
        self.account_id = account_id

    def json(self):
        return {
            'id': self.id,
            'date': self.date,
            'amount': self.amount
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
