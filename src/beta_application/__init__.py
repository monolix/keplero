from flask_restplus import Api
from flask import Flask

from .authorizing import api as auth

app = Flask(__name__)

api = Api(
    app,
    title="Keplero",
    description="REST API of the Keplero Coin System"
)

api.add_namespace(auth)
