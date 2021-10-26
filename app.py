from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.login import Login, Balance
from db import db
from models.bank import BankModel
from models.account import AccountModel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.secret_key = '1234'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()
    bank = BankModel('Privat')
    bank.save_to_db()
    account = AccountModel('Yarema', '1234', '5167', bank.id, 1544)
    account.save_to_db()


api.add_resource(Login, '/login')
api.add_resource(Balance, '/balance')

jwt = JWTManager(app)


@jwt.additional_claims_loader
def add_claims_loader(identity):
    return {'_id': True}


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
    app.run(port=5000, debug=True)
