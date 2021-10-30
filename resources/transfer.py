import json
from datetime import datetime

from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from pydantic import BaseModel, ValidationError

from models.bank import BankModel
from models.account import AccountModel
from models.transfer import TransferModel


class TransferSchema(BaseModel):
    destinationCard: str
    amount: float


class Transfer(Resource):
    @jwt_required()
    def post(self):
        account: AccountModel = AccountModel.get_by_id(get_jwt_identity())
        try:
            transfer_schema: TransferSchema = TransferSchema.parse_raw(json.dumps(request.get_json()))
        except ValidationError:
            return {"message": "invalid arguments"}, 400
        if account.balance < transfer_schema.amount:
            return {"message": "not enough money on account"}
        if not AccountModel.is_card_valid(transfer_schema.destinationCard):
            return {"message": "invalid destination card"}
        destination_account: AccountModel = AccountModel.get_by_card(transfer_schema.destinationCard)
        account.balance -= transfer_schema.amount
        destination_account.balance += transfer_schema.amount
        transfer = TransferModel(transfer_schema.destinationCard, transfer_schema.amount, account.id)
        transfer.save_to_db()
        return transfer.json()


class Transfers(Resource):
    @jwt_required()
    def get(self):
        account: AccountModel = AccountModel.get_by_id(get_jwt_identity())
        return account.get_transfers()
