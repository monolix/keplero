from . import s
from .models import User
from flask import Blueprint, render_template
from itsdangerous import SignatureExpired

views = Blueprint("views", __name__)

@views.route("/verify-email/<token>")
def verifyAccount(token):
    try:
        email = s.loads(token, salt="verify-account", max_age=600)
        user = User.query.filter_by(email=email).first()
        user.status = "normal"
        user.save()
        return render_template("verified.html", verified=True)
    except SignatureExpired:
        return render_template("verified.html", verified=False)


@views.route("/verify-access/<id>/<ip>", methods=["POST"])
def verifyAccess(id, ip):
    user = User.query.filter_by(id=id).first()
    if user is None:
        abort(404)
    
    user.whitelist.append(str(ip))
    user.save()
