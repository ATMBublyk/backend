import json
from datetime import datetime

from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from pydantic import BaseModel, ValidationError

from db import db
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
            return {"message": "not enough money on account"}, 400
        if account.card_number == transfer_schema.destinationCard:
            return {"message": "you can't send money for your own card"}, 400
        if not AccountModel.is_card_valid(transfer_schema.destinationCard):
            return {"message": "invalid destination card"}, 400
        return self.make_transfer(get_jwt_identity(), transfer_schema.destinationCard, transfer_schema.amount, False).json()

    @staticmethod
    def make_transfer(account_id, destination_card, amount, is_regular, is_auto=False) -> TransferModel:
        # todo session from another thread
        account = AccountModel.get_by_id(account_id)
        destination_account: AccountModel = AccountModel.get_by_card(destination_card)
        account.balance -= amount
        destination_account.balance += amount
        if destination_account.have_surpluses_account:
            if destination_account.balance > destination_account.surpluses_max_balance:
                surpluses_amount = destination_account.balance - destination_account.surpluses_max_balance
                Transfer.make_transfer(destination_account.id, destination_account.surpluses_destination_card,
                                   surpluses_amount, False, True)
                destination_account.balance = destination_account.surpluses_max_balance
        date = datetime.now()
        transfer = TransferModel(date, destination_card, amount, account.id, is_regular, is_auto)
        transfer.save_to_db()
        return transfer


class Transfers(Resource):
    @jwt_required()
    def get(self):
        account: AccountModel = AccountModel.get_by_id(get_jwt_identity())
        return account.get_transfers()
