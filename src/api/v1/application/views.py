from . import s
from .models import User
from flask import Blueprint, render_template
from itsdangerous import SignatureExpired

views = Blueprint("views", __name__)

@views.route("/verify/<token>")
def verifyAccount(token):
    try:
        email = s.loads(token, salt="verify-account", max_age=600)
        user = User.query.filter_by(email=email).first()
        user.status = "normal"
        user.save()
        return render_template("verified.html", verified=True)
    except SignatureExpired:
        return render_template("verified.html", verified=False)
