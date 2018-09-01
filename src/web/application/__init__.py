from flask import Flask

app = Flask(__name__)

app.config["API_ENDPOINT"] = "http://api"

from .views import *
from .routes import *
