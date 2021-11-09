import json
from datetime import timedelta

from flask_restful import Resource, request
from flask_jwt_extended import create_access_token, jwt_required
from pydantic import BaseModel, ValidationError

from models.admin import AdminModel
from models.bank import BankModel
from models.account import AccountModel


class AdminLoginSchema(BaseModel):
    login: str
    password: str


EXPIRES_DELTA = timedelta(hours=1)


class AdminRegister(Resource):
    def post(self):
        admins: list = AdminModel.get_admins()
        if admins:
            return {"message": "can't register more than one admin"}, 400
        try:
            admin_login_schema: AdminLoginSchema = AdminLoginSchema.parse_raw(json.dumps(request.get_json()))
        except ValidationError:
            return {"message": "invalid arguments"}, 400
        admin_model: AdminModel = AdminModel(admin_login_schema.login, admin_login_schema.password)
        admin_model.save_to_db()
        return {"message": "admin has been successfully registered"}, 201


class AdminLogin(Resource):
    def post(self):
        try:
            admin_login_schema: AdminLoginSchema = AdminLoginSchema.parse_raw(json.dumps(request.get_json()))
        except ValidationError:
            return {"message": "invalid arguments"}, 400
        admins: list = AdminModel.get_admins()
        if not admins:
            return {"message": "there is no admins"}, 400
        admin: AdminModel = admins[0]
        if admin_login_schema.login == admin.login and admin_login_schema.password == admin.password:
            return {"accessToken": create_access_token(1, expires_delta=EXPIRES_DELTA)}
        else:
            return {"message": "invalid credentials"}, 400


class Banks(Resource):
    @jwt_required()
    def get(self):
        return BankModel.get_banks()


class BankRegisterSchema(BaseModel):
    name: str


class BankRegister(Resource):
    @jwt_required()
    def get(self, id):
        bank: BankModel = BankModel.get_by_id(id)
        if bank is None:
            return {"message": f"there is no bank with id {id}"}
        return bank.json()

    @jwt_required()
    def post(self):
        try:
            bank_register_schema: BankRegisterSchema = BankRegisterSchema.parse_raw(json.dumps(request.get_json()))
        except ValidationError:
            return {"message": "invalid arguments"}, 400
        if BankModel.get_by_name(bank_register_schema.name) is not None:
            return {"message": f"bank with name {bank_register_schema.name} exists"}
        bank = BankModel(bank_register_schema.name)
        bank.save_to_db()
        return {"bankId": bank.id}, 201

    @jwt_required()
    def delete(self, id):
        bank: BankModel = BankModel.get_by_id(id)
        if bank is None:
            return {"message": f"bank with id {id} does not exist"}
        if bank.has_accounts():
            return {"message": "can't delete bank because it has active accounts"}, 400
        bank.delete_from_db()
        return {"message": "bank deleted successfully"}, 200


class AccountRegisterSchema(BaseModel):
    cardNumber: str
    pin: str
    name: str
    bankId: int


class AccountRegister(Resource):
    @jwt_required()
    def get(self, id):
        account: AccountModel = AccountModel.get_by_id(id)
        if account is None:
            return {"message": f"there is no account with id {id}"}
        return account.json_admin()

    @jwt_required()
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

    @jwt_required()
    def delete(self, id):
        try:
            AccountModel.get_by_id(id).delete_from_db()
        except AttributeError:
            return {"message": f"user with id {id} does not exist"}
        return {"message": "user deleted successfully"}
