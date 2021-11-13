import os
from datetime import timedelta

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api

from blacklist import BLACKLIST
from db import db
from resources.card_info import CardInfo
from resources.deposit import Deposit, Deposits
from resources.login import Login
from resources.logout import Logout
from resources.admin_panel import AccountRegister, BankRegister, Banks, AdminRegister, AdminLogin
from resources.regular_transfer import RegularTransfer, RegularTransfers
from resources.surpluses_account import SurplusesAccount
from resources.transfer import Transfer, Transfers
from resources.withdrawal import Withdrawal, Withdrawals

ACCESS_EXPIRES = timedelta(minutes=10)
app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "http://localhost"}})
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = ACCESS_EXPIRES
app.config['JWT_SECRET_KEY'] = '1234'
api = Api(app)

jwt = JWTManager(app)


@app.before_first_request
def create_tables():
    db.create_all()


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_headers, jwt_payload):
    return jwt_payload['jti'] in BLACKLIST


# admin panel
api.add_resource(AdminRegister, '/admin-register')
api.add_resource(AdminLogin, '/admin-login')
api.add_resource(BankRegister, '/bank', '/bank/<int:id>')
api.add_resource(AccountRegister, '/account', '/account/<int:id>')
api.add_resource(Banks, '/banks')
# api
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(CardInfo, '/card-info')
api.add_resource(Deposit, '/deposit')
api.add_resource(Deposits, '/deposits')
api.add_resource(Withdrawal, '/withdrawal')
api.add_resource(Withdrawals, '/withdrawals')
api.add_resource(Transfer, '/transfer')
api.add_resource(Transfers, '/transfers')
api.add_resource(RegularTransfer, '/regular-transfer', '/regular-transfer/<int:id>')
api.add_resource(RegularTransfers, '/regular-transfers')
api.add_resource(SurplusesAccount, '/surpluses-account')


@jwt.additional_claims_loader
def add_claims_loader(identity):
    return {'_id': True}


@jwt.revoked_token_loader
def revoked_token(arg1, arg2):
    return {"message": "token has been revoked"}


@jwt.expired_token_loader
def expired_token_callback(arg1, arg2):
    return jsonify({
        'description': 'The token has expired.',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(arg):
    return jsonify({
        'description': 'What the fuck are you doing???',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def unauthorized_callback(arg):
    return jsonify({
        'description': 'You need to send JWT token',
        'error': 'unauthorized'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback(arg1, arg2):
    return jsonify({
        'description': 'Token is no longer valid (you have logged out)',
        'error': 'revoked_token'
    }), 401


db.init_app(app)
if __name__ == '__main__':
    app.run(port=5000, debug=False)
