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
        return None
        # return self.make_transfer(get_jwt_identity(), transfer_schema.destinationCard, transfer_schema.amount).json()

    # @staticmethod
    # def make_transfer(account_id, destination_card, amount) -> TransferModel:
    #     account = AccountModel.get_by_id(account_id)
    #     destination_account: AccountModel = AccountModel.get_by_card(destination_card)
    #     account.balance -= amount
    #     destination_account.balance += amount
    #     date = datetime.now()
    #     transfer = TransferModel(date, destination_card, amount, account.id)
    #     transfer.save_to_db()


class Transfers(Resource):
    @jwt_required()
    def get(self):
        account: AccountModel = AccountModel.get_by_id(get_jwt_identity())
        return account.get_transfers()
