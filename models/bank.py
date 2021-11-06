from db import db
from exceptions.exceptions import WrongPinException


class BankModel(db.Model):
    __tablename__ = 'banks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    accounts = db.relationship('AccountModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def start_session(self, card_number, pin):
        for account in self.accounts.all():
            if account.card_number == card_number and account.pin == pin:
                return account.id
        else:
            raise WrongPinException()

    def get_balance_by_id(self, _id):
        for account in self.accounts.all():
            if account.id == _id:
                return account.balance

    def has_accounts(self):
        return self.accounts.all() is not None

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
