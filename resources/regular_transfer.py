import json
from datetime import datetime

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, request
from pydantic import BaseModel, ValidationError

from models.account import AccountModel
from models.regular_transfer import RegularTransferModel


class RegularTransferSchema(BaseModel):
    destinationCard: str
    amount: int
    periodicity: str
    firstPaymentDate: str


class RegularTransfer(Resource):
    @jwt_required()
    def post(self):
        account: AccountModel = AccountModel.get_by_id(get_jwt_identity())
        try:
            regular_transfer_schema = RegularTransferSchema.parse_raw(json.dumps(request.get_json()))
        except ValidationError:
            return {"message": "invalid arguments"}, 400
        first_payment_date = datetime.strptime(regular_transfer_schema.firstPaymentDate, "%Y-%m-%dT%H:%M:%S.%f")
        if first_payment_date < datetime.now():
            return {"message": "invalid date: you should set date in the future"}
        periodicity = regular_transfer_schema.periodicity
        amount = regular_transfer_schema.amount
        destination_card = regular_transfer_schema.destinationCard
        if not AccountModel.is_card_valid(destination_card):
            return {"message": "invalid destination card"}
        regular_transfer = RegularTransferModel(destination_card, amount, periodicity, first_payment_date, account.id)
        return regular_transfer.json()
