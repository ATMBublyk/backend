import json
from datetime import datetime

from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from pydantic import BaseModel, ValidationError

from models.bank import BankModel
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
