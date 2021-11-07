import json

from flask_restful import Resource, request
from flask_jwt_extended import create_access_token
from pydantic import BaseModel, ValidationError

from models.bank import BankModel
from models.account import AccountModel


class AccountRegisterSchema(BaseModel):
    cardNumber: str
    pin: str
    name: str
    bankId: int


class AccountRegister(Resource):
    def get(self, id):
        account: AccountModel = AccountModel.get_by_id(id)
        if account is None:
            return {"message": f"there is no account with id {id}"}
        return account.json()

    def post(self):
        try:
            account_register_schema: AccountRegisterSchema = AccountRegisterSchema.parse_raw(
                json.dumps(request.get_json()))
        except ValidationError:
            return {"message": "invalid arguments"}, 400
        if AccountModel.get_by_card(account_register_schema.cardNumber) is not None:
            return {"message": f"user with {account_register_schema.cardNumber} card number exists"}, 400
        if BankModel.get_by_id(account_register_schema.bankId) is None:
            return {"message": f"there is no bank with id {account_register_schema.bankId}"}, 400
        account = AccountModel(account_register_schema.name, account_register_schema.cardNumber,
                               account_register_schema.pin, account_register_schema.bankId)
        account.save_to_db()
        return {"message": "user created successfully"}, 201

    def delete(self, id):
        try:
            AccountModel.get_by_id(id).delete_from_db()
        except AttributeError:
            return {"message": f"user with id {id} does not exist"}
        return {"message": "user deleted successfully"}


class BankRegisterSchema(BaseModel):
    name: str


class BankRegister(Resource):
    def get(self, id):
        bank: BankModel = BankModel.get_by_id(id)
        if bank is None:
            return {"message": f"there is no bank with id {id}"}
        return bank.json()

    def post(self):
        try:
            bank_register_schema: BankRegisterSchema = BankRegisterSchema.parse_raw(json.dumps(request.get_json()))
        except ValidationError:
            return {"message": "invalid arguments"}, 400
        if BankModel.get_by_id(bank_register_schema.name) is not None:
            return {"message": f"bank with name {bank_register_schema.name} exists"}
        bank = BankModel(bank_register_schema.name)
        bank.save_to_db()
        return {"bankId": bank.id}, 201

    def delete(self, id):
        bank: BankModel = BankModel.get_by_id(id)
        if bank is None:
            return {"message": f"bank with id {id} does not exist"}
        if bank.has_accounts():
            return {"message": "can't delete bank because it has active accounts"}, 403
        bank.delete_from_db()
        return {"message": "bank deleted successfully"}, 204
