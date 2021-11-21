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

    def json_simple(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def json(self):
        return {
            "name": self.name,
            "accounts": [account.json_admin() for account in self.accounts]
        }

    def start_session(self, card_number, pin):
        for account in self.accounts.all():
            if account.card_number == card_number and account.pin == pin:
                return account.id
        else:
            raise WrongPinException()

    def has_accounts(self):
        return bool(self.accounts.all())

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_banks(cls):
        return [bank.json_simple() for bank in cls.query.all()]
