import json
from datetime import datetime

from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from pydantic import BaseModel, ValidationError

from models.bank import BankModel
from models.account import AccountModel
from models.deposit import DepositModel
from resources.transfer import Transfer


class DepositSchema(BaseModel):
    amount: float


class Deposit(Resource):
    @jwt_required()
    def post(self):
        account: AccountModel = AccountModel.get_by_id(get_jwt_identity())
        try:
            deposit_schema: DepositSchema = DepositSchema.parse_raw(json.dumps(request.get_json()))
        except ValidationError:
            return {"message": "invalid arguments"}, 400
        if deposit_schema.amount is None:
            return {"message": "amount can't be null"}
        account.balance += deposit_schema.amount
        if account.have_surpluses_account and (account.balance > account.surpluses_max_balance):
            surpluses_amount = account.balance - account.surpluses_max_balance
            Transfer.make_transfer(account.id, account.surpluses_destination_card, surpluses_amount, False, True)
        deposit = DepositModel(datetime.utcnow(), deposit_schema.amount, account.id)
        deposit.save_to_db()
        return deposit.json()


class Deposits(Resource):
    @jwt_required()
    def get(self):
        account: AccountModel = AccountModel.get_by_id(get_jwt_identity())
        return account.get_deposits()
