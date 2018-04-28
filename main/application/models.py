from flask_restplus import fields
from .api import api

models = {
    "account": api.model("Account Credentials", {
        "id": fields.String("The Account's ID."),
        "password": fields.String("The Account's password.")
    })
}
