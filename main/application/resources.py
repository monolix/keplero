from .api import api
from .models import models
from .db_controller import getHashedPassword, createSession, hashTok
from flask_restplus import Resource

@api.route("/authorize")
class Auth(Resource):
    @api.expect(models["account"])
    def post(self):
        if set(['id', 'password']) == set(api.payload.keys()):
            password = api.payload['password']
            id = api.payload['id']
            db_password = getHashedPassword(id)
            if hashTok(password) == db_password:
                id, now, token = createSession(id)
                return {
                    'ok': True,
                    'response': {
                        'token': token,
                        'when': now
                    }
                }
            else:
                return {
                    'ok': False,
                    'error': '<auth:invalid_credentials>'
                }
        else:
            return {
                'ok': False,
                'error': '<syntax:invalid_json>'
            }
