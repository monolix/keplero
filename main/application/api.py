from flask_restplus import Api
from . import app

api = Api(app)

from .resources import *
