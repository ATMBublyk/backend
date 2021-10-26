import json

from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from pydantic import BaseModel, ValidationError
from flask_pydantic import validate

from ATM.atm import ATM
from models.bank import BankModel
from models.account import AccountModel


class LoginSchema(BaseModel):
    cardNumber: str
    pin: str


class BalanceSchema(BaseModel):
    id: float


atm = ATM()


class Login(Resource):
    def post(self):
        try:
            login: LoginSchema = LoginSchema.parse_raw(json.dumps(request.get_json()))
        except ValidationError:
            return {"message": "wrong args"}
        bank = BankModel.get_by_name("Privat")
        id = bank.start_session(login.cardNumber, login.pin)
        access_token = create_access_token(identity=id)
        return {'access_token': access_token}, 200


class Balance(Resource):
    @jwt_required()
    def get(self):
        account: AccountModel = AccountModel.get_by_id(get_jwt_identity())
        bank = BankModel.get_by_id(account.bank_id)
        balance = bank.get_balance_by_id(account.id)
        return {'balance': balance}
