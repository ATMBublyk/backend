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
    isRegular: bool


class Transfer(Resource):
    @jwt_required()
    def post(self):
        account: AccountModel = AccountModel.get_by_id(get_jwt_identity())
        if account is None:
            return {"message": "incorrect account id"}
        try:
            json_dict = request.get_json()
            if json_dict is None:  # for regular payments executor
                json_dict = dict(request.form)
            transfer_schema: TransferSchema = TransferSchema.parse_raw(json.dumps(json_dict))
        except ValidationError:
            return {"message": "Invalid arguments."}, 400
        if transfer_schema.amount is None:
            return {"message": "Amount can't be null."}
        if account.balance < transfer_schema.amount:
            return {"message": "Not enough money on the account."}, 400
        if account.card_number == transfer_schema.destinationCard:
            return {"message": "You can't send money to your own card."}, 400
        if not AccountModel.is_card_valid(transfer_schema.destinationCard):
            return {"message": "Invalid destination card."}, 400
        return self.make_transfer(get_jwt_identity(), transfer_schema.destinationCard, transfer_schema.amount,
                                  transfer_schema.isRegular).json(), 201

    @staticmethod
    def make_transfer(account_id, card, amount, is_regular, is_auto=False) -> TransferModel:
        # todo session from another thread
        account: AccountModel = AccountModel.get_by_id(account_id)
        destination_account: AccountModel = AccountModel.get_by_card(card)
        account.balance -= amount
        destination_account.balance += amount
        if destination_account.have_surpluses_account:
            if destination_account.balance > destination_account.surpluses_max_balance:
                surpluses_amount = destination_account.balance - destination_account.surpluses_max_balance
                Transfer.make_transfer(destination_account.id, destination_account.surpluses_destination_card,
                                       surpluses_amount, False, True)
                destination_account.balance = destination_account.surpluses_max_balance
        date = datetime.utcnow()
        transfer = TransferModel(date, card, amount, account.id, is_regular, is_auto, True)
        destination_transfer = TransferModel(date, account.card_number, amount, destination_account.id, False, False,
                                             False)
        transfer.save_to_db()
        destination_transfer.save_to_db()
        return transfer


class Transfers(Resource):
    @jwt_required()
    def get(self):
        account: AccountModel = AccountModel.get_by_id(get_jwt_identity())
        return account.get_transfers()
