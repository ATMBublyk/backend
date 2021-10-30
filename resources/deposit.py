import json
from datetime import datetime

from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from pydantic import BaseModel, ValidationError

from models.bank import BankModel
from models.account import AccountModel
from models.deposit import DepositModel


class DepositSchema(BaseModel):
    amount: float


class Deposit(Resource):
    @jwt_required()
    def post(self):  # todo surpluses
        account: AccountModel = AccountModel.get_by_id(get_jwt_identity())
        try:
            deposit_schema: DepositSchema = DepositSchema.parse_raw(json.dumps(request.get_json()))
        except ValidationError:
            return {"message": "invalid arguments"}, 400
        account.balance += deposit_schema.amount
        deposit = DepositModel(datetime.now(), deposit_schema.amount, account.id)
        deposit.save_to_db()
        return deposit.json()


class Deposits(Resource):
    @jwt_required()
    def get(self):
        account: AccountModel = AccountModel.get_by_id(get_jwt_identity())
        return account.get_deposits()
