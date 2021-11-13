import json
from datetime import datetime

from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from pydantic import BaseModel, ValidationError

from models.bank import BankModel
from models.account import AccountModel
from models.withdrawal import WithdrawalModel


class WithdrawalSchema(BaseModel):
    amount: float


class Withdrawal(Resource):
    @jwt_required()
    def post(self):
        account: AccountModel = AccountModel.get_by_id(get_jwt_identity())
        try:
            withdrawal_schema: WithdrawalSchema = WithdrawalSchema.parse_raw(json.dumps(request.get_json()))
        except ValidationError:
            return {"message": "Invalid arguments."}, 400
        if withdrawal_schema.amount is None:
            return {"message": "Amount can't be null."}, 400
        if account.balance < withdrawal_schema.amount:
            return {"message": "Not enough money for this transaction."}, 403
        account.balance -= withdrawal_schema.amount
        withdrawal = WithdrawalModel(withdrawal_schema.amount, datetime.utcnow(), account.id)
        withdrawal.save_to_db()
        return withdrawal.json()


class Withdrawals(Resource):
    @jwt_required()
    def get(self):
        account: AccountModel = AccountModel.get_by_id(get_jwt_identity())
        return account.get_withdrawals()
