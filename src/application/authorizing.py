from flask_restplus import Namespace, Resource, fields
from .utils.database import getHashedPassword, createSession, hashTok

api = Namespace("authorize", description="Login related operations.")

credentials = api.model("Account Credentials", {
    "id": fields.String("123456789", required=True, description="The Account's ID."),
    "password": fields.String("log_me9452!#", required=True, description="The Account's password.")
})

@api.route("/getToken")
class GetToken(Resource):
    @api.expect(credentials)
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
