from flask import Flask
from flask_mongoalchemy import MongoAlchemy
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__)

app.config.from_pyfile("config.cfg")

db = MongoAlchemy(app)
mail = Mail(app)
bcrypt = Bcrypt(app)
serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])


# Load Models & Errors
from .models import *
from .errors import *

# Load Blueprints
from .views import views
from .authorization import auth

app.register_blueprint(views)
app.register_blueprint(auth, url_prefix="/authorization")
