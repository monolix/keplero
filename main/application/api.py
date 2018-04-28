from . import api
from flask_restplus import Resource

@api.route("/authorize")
class Auth(Resource):
    def post(self, *body):
        return body

    def get(self, *args):
        return "GETTER"
