from . import bcrypt, mail, s
from .models import User
from flask import Blueprint, request, abort, render_template, jsonify
from flask_mail import Message

auth = Blueprint("authorization", __name__)

@auth.route("/register", methods=["POST"])
def registerUser():
    payload = request.get_json()
    required = ["id", "password", "email", "username"]
    if set(payload) >= set(required):
        id = payload["id"]
        password = payload["password"]
        email = payload["email"]
        username = payload["username"]

        user = User.query.filter_by(id=id).first()

        if user is not None:
            return abort(403)
        
        user = User.query.filter_by(email=email).first()

        if user is not None:
            return abort(403)

        user = User(
            id = id,
            password = password,
            email = email,
            username = username,
            balance = 0,
            status = "unverified"
        )

        user.save()

        msg = Message(
            "Verify your Account"
        )

        token = s.dumps(email, salt="verify-account")

        msg.html = render_template("emails/verify.html", username=username, token=token)

        mail.send(msg)

        return jsonify({
            "ok": True,
            "result": {
                "description": "Account Verification sent via Email."
            }
        })
    else:
        return abort(400)

