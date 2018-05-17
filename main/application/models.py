from flask_restplus import fields, Namespace
from .api import api

auth_ns = Namespace('Authorizing', description="Login related operations.")

models = {
    "account": api.model("Account Credentials", {
        "id": fields.String(required=True, "123456789"),
        "password": fields.String(required=True, "login_me!")
    })
}

api.add_namespace(auth_ns)
