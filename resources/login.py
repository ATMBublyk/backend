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
            json_dict = request.get_json()
            if json_dict is None:  # need for regular payments executor
                json_dict = dict(request.form)
            login_schema: LoginSchema = LoginSchema.parse_raw(json.dumps(json_dict))
        except ValidationError:
            return {"message": "Invalid arguments."}, 400
        try:
            bank_id = AccountModel.get_bank_id(login_schema.cardNumber)
        except AttributeError:
            return {"message": "Account doesn't exist."}, 400
        bank: BankModel = BankModel.get_by_id(bank_id)
        try:
            id = bank.start_session(login_schema.cardNumber, login_schema.pin)
        except WrongPinException:
            return {"message": "Invalid credentials."}, 400
        access_token = create_access_token(identity=id, expires_delta=EXPIRES_DELTA)
        return {'accessToken': access_token}, 200
