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
from .users import user
from .actions import action
from .about import about

app.register_blueprint(views)
app.register_blueprint(auth, url_prefix="/authorization")
app.register_blueprint(user, url_prefix="/users")
app.register_blueprint(action, url_prefix="/actions")
app.register_blueprint(help, url_prefix="/about")
