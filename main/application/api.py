from flask_restplus import Api
from . import app

api = Api(
    app,
    version="0.01",
    description="The official JSON REST API for the Keplero Coin System."
)

from .resources import *
