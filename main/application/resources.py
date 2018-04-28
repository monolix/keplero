from .api import api
from .models import models
from flask_restplus import Resource

@api.route("/authorize")
class Auth(Resource):
    @api.expect(models["account"])
    def post(self):
        return api.payload["id"]
