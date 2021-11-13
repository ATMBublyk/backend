import json
from datetime import datetime

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, request
from pydantic import BaseModel, ValidationError

from models.account import AccountModel
from models.regular_transfer import RegularTransferModel


class RegularTransferSchema(BaseModel):
    destinationCard: str
    amount: float
    periodicity: str
    firstPaymentDate: str


class RegularTransfers(Resource):
    @jwt_required()
    def get(self):
        account: AccountModel = AccountModel.get_by_id(get_jwt_identity())
        return account.get_regular_transfers()


class RegularTransfer(Resource):
    @jwt_required()
    def get(self, id):
        account: AccountModel = AccountModel.get_by_id(get_jwt_identity())
        try:
            regular_transfer = account.get_regular_transfer_by_id(id).json()
        except AttributeError:
            return {"message": f"There is no regular payment with id {id}."}
        return regular_transfer

    @jwt_required()
    def delete(self, id):
        account: AccountModel = AccountModel.get_by_id(get_jwt_identity())
        regular_transfer = account.get_regular_transfer_by_id(id)
        output_json = regular_transfer.json()
        regular_transfer.delete_from_db()
        return output_json

    @jwt_required()
    def put(self, id):
        account: AccountModel = AccountModel.get_by_id(get_jwt_identity())
        try:
            regular_transfer_schema: RegularTransferSchema = RegularTransferSchema.parse_raw(
                json.dumps(request.get_json()))
        except ValidationError:
            return {"message": "Invalid arguments."}, 400
        periodicity = regular_transfer_schema.periodicity
        amount = regular_transfer_schema.amount
        destination_card = regular_transfer_schema.destinationCard
        first_payment_date_str = regular_transfer_schema.firstPaymentDate
        json_error = self.validate_data(periodicity, amount, destination_card, first_payment_date_str,
                                        account.card_number)
        if json_error is not None:
            return json_error
        first_payment_date = datetime.strptime(first_payment_date_str, "%Y-%m-%dT%H:%M:%S.%f")
        regular_transfer: RegularTransferModel = RegularTransferModel.get_by_id(id)
        regular_transfer.periodicity = periodicity
        regular_transfer.amount = amount
        regular_transfer.destination_card = destination_card
        regular_transfer.first_payment_date = first_payment_date
        regular_transfer.save_to_db()
        return regular_transfer.json()

    @jwt_required()
    def post(self):
        account: AccountModel = AccountModel.get_by_id(get_jwt_identity())
        try:
            regular_transfer_schema: RegularTransferSchema = RegularTransferSchema.parse_raw(
                json.dumps(request.get_json()))
        except ValidationError:
            return {"message": "Invalid arguments."}, 400
        periodicity = regular_transfer_schema.periodicity
        amount = regular_transfer_schema.amount
        destination_card = regular_transfer_schema.destinationCard
        first_payment_date_str = regular_transfer_schema.firstPaymentDate
        json_error = self.validate_data(periodicity, amount, destination_card, first_payment_date_str,
                                        account.card_number)
        if json_error is not None:
            return json_error
        first_payment_date = datetime.strptime(first_payment_date_str, "%Y-%m-%dT%H:%M:%S.%f")
        regular_transfer = RegularTransferModel(destination_card, amount, periodicity, first_payment_date, account.id)
        regular_transfer.save_to_db()
        return regular_transfer.json()

    @classmethod
    def validate_data(cls, periodicity: str, amount: float, destination_card: str, first_payment_date_str: str,
                      sender_card):
        try:
            first_payment_date = datetime.strptime(first_payment_date_str, "%Y-%m-%dT%H:%M:%S.%f")
        except ValueError:
            return {"message": "Incorrect date format."}, 400
        if first_payment_date < datetime.utcnow():
            return {"message": "Invalid date: you should set the future date."}, 400
        if not AccountModel.is_card_valid(destination_card):
            return {"message": "Invalid destination card."}, 400
        if amount is None:
            return {"message": "Amount can't be null."}, 400
        if amount <= 0:
            return {"message": "Amount can't be negative."}, 400
        if sender_card == destination_card:
            return {"message": "You can't send money to your own card."}, 400
        if not cls.validate_periodicity(periodicity):
            return {"message": f"There is no {periodicity} periodicity. Use everyday, weekly, monthly or annually."}, 400

    @staticmethod
    def validate_periodicity(periodicity) -> bool:
        valid_periodicities = ['everyday', 'weekly', 'monthly', 'annually']
        is_valid = False
        for valid_periodicity in valid_periodicities:
            if periodicity == valid_periodicity:
                is_valid = True
        return is_valid
