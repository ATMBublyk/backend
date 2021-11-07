import json
from datetime import timedelta

from flask_restful import Resource, request
from flask_jwt_extended import create_access_token
from pydantic import BaseModel, ValidationError

from exceptions.exceptions import WrongPinException
from models.bank import BankModel
from models.account import AccountModel

EXPIRES_DELTA = timedelta(minutes=10)


class LoginSchema(BaseModel):
    cardNumber: str
    pin: str


class Login(Resource):
    def post(self):
        try:
            login_schema: LoginSchema = LoginSchema.parse_raw(json.dumps(request.get_json()))
        except ValidationError:
            return {"message": "invalid arguments"}, 400
        try:
            bank_id = AccountModel.get_bank_id(login_schema.cardNumber)
        except AttributeError:
            return {"message": "account does not exist"}, 400
        bank: BankModel = BankModel.get_by_id(bank_id)
        try:
            id = bank.start_session(login_schema.cardNumber, login_schema.pin)
        except WrongPinException:
            return {"message": "invalid credentials"}, 400
        access_token = create_access_token(identity=id, expires_delta=EXPIRES_DELTA)
        return {'accessToken': access_token}, 200
