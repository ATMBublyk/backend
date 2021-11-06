from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.account import AccountModel
from models.bank import BankModel


class Balance(Resource):
    @jwt_required()
    def get(self):
        account: AccountModel = AccountModel.get_by_id(get_jwt_identity())
        balance = account.get_balance()
        card_number = account.card_number
        bank = BankModel.get_by_id(account.bank_id)
        bank_name = bank.bank_name
        return {
            'cardNumber': card_number,
            'balance': balance,
            'bankName': bank_name
        }
