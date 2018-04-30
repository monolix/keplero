from flask import Flask

app = Flask(__name__)

app.config["DATABASE_PATH"] = "/home/emanuele/projects/keplero/main/database/users.db"

from .db_controller import *
from .api import *
