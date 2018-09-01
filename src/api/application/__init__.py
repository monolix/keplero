from flask import Flask
from flask_mongoalchemy import MongoAlchemy


app = Flask(__name__)

app.config.from_pyfile("config.cfg")

db = MongoAlchemy(app)

from .routes import *
from .modules import *
