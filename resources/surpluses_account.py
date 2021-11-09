import json
from datetime import datetime

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, request
from pydantic import BaseModel, ValidationError

from models.account import AccountModel
from models.regular_transfer import RegularTransferModel


class SurplusesAccountSchema(BaseModel):
    destinationCard: str
    maxBalance: float


class SurplusesAccount(Resource):
    @jwt_required()
    def post(self):
        account: AccountModel = AccountModel.get_by_id(get_jwt_identity())
        try:
            surpluses_account_schema: SurplusesAccountSchema = SurplusesAccountSchema.parse_raw(
                json.dumps(request.get_json()))
        except ValidationError:
            return {"message": "invalid arguments"}, 400
        destination_card = surpluses_account_schema.destinationCard
        max_balance = surpluses_account_schema.maxBalance
        if max_balance <= 0:
            return {"message": "max balance can't be negative or 0"}, 400
        if not AccountModel.is_card_valid(destination_card):
            return {"message": "invalid destination card"}, 400
        if account.card_number == surpluses_account_schema.destinationCard:
            return {"message": "you can't send money for your own card"}, 400
        account.surpluses_destination_card = destination_card
        account.surpluses_max_balance = max_balance
        account.have_surpluses_account = True
        account.save_to_db()
        return {
            "destinationCard": destination_card,
            "maxBalance": max_balance
        }

    @jwt_required()
    def get(self):
        account: AccountModel = AccountModel.get_by_id(get_jwt_identity())
        if not account.have_surpluses_account:
            return {"message": "account don't have surpluses account"}, 400
        return {
            "destinationCard": account.surpluses_destination_card,
            "maxBalance": account.surpluses_max_balance
        }

    @jwt_required()
    def put(self):
        account: AccountModel = AccountModel.get_by_id(get_jwt_identity())
        try:
            surpluses_account_schema: SurplusesAccountSchema = SurplusesAccountSchema.parse_raw(
                json.dumps(request.get_json()))
        except ValidationError:
            return {"message": "invalid arguments"}, 400
        destination_card = surpluses_account_schema.destinationCard
        max_balance = surpluses_account_schema.maxBalance
        if max_balance <= 0:
            return {"message": "max balance can't be negative or 0"}, 400
        if not AccountModel.is_card_valid(destination_card):
            return {"message": "invalid destination card"}, 400
        if account.card_number == surpluses_account_schema.destinationCard:
            return {"message": "you can't send money for your own card"}, 400
        account.surpluses_destination_card = destination_card
        account.surpluses_max_balance = max_balance
        account.have_surpluses_account = True
        account.save_to_db()
        return {
            "destinationCard": destination_card,
            "maxBalance": account.surpluses_max_balance
        }

    @jwt_required()
    def delete(self):
        account: AccountModel = AccountModel.get_by_id(get_jwt_identity())
        if not account.have_surpluses_account:
            return {"message": "this account don't have surpluses account"}, 400
        destination_card = account.surpluses_destination_card
        max_balance = account.surpluses_max_balance
        account.surpluses_destination_card = ""
        account.surpluses_max_balance = 0
        account.have_surpluses_account = False
        account.save_to_db()
        return {
            "destinationCard": destination_card,
            "maxBalance": max_balance
        }
