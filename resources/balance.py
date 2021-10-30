from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from pydantic import BaseModel

from models.account import AccountModel


class BalanceSchema(BaseModel):
    id: float


class Balance(Resource):
    @jwt_required()
    def get(self):
        account: AccountModel = AccountModel.get_by_id(get_jwt_identity())
        balance = account.get_balance()
        return {'balance': balance}
