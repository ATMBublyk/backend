from datetime import timedelta

from flask_jwt_extended import jwt_required, get_jwt
from flask_restful import Resource

from blacklist import BLACKLIST


class Logout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']  # jti is "JWT ID", a unique identifier for a JWT.
        BLACKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200
