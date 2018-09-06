from . import bcrypt, mail, s
from .models import User, Session
from time import time
from flask import Blueprint, request, abort, render_template, jsonify
from flask_mail import Message

auth = Blueprint("authorization", __name__)

@auth.route("/register", methods=["POST"])
def registerUser():
    payload = request.get_json()
    required = ["id", "password", "email", "username"]

    if not set(payload) >= set(required):
        return abort(400)
    
    id = payload["id"]
    password = payload["password"]
    email = payload["email"]
    username = payload["username"]
    
    user = User.query.filter_by(id=id).first()

    if user != None:
        return abort(409)
        
    user = User.query.filter_by(email=email).first()

    if user != None:
        return abort(409)
        

    user = User(
        id = id,
        password = bcrypt.generate_password_hash(password),
        email = email,
        username = username,
        balance = 0,
        status = "unverified"
    )

    user.save()

    msg = Message(
        "Verify your Account",
        recipients=[email]
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

@auth.route("/login", methods=["POST"])
def loginUser():
    payload = request.get_json()
    required = ["id", "password"]
    
    if not set(required) >= set(payload):
        return abort(400)

    id = payload["id"]
    password = payload["password"]

    user = User.query.filter_by(id=id).first()

    if not bcrypt.check_password_hash(user.password, password):
        return abort(401)
    
    if user.status == "unverified":
        return abort(401)

    session_token = s.dumps(user.id + str(time()), salt="session-token")[:32]

    session = Session(id=user.id, token=session_token)

    session.save()

    return jsonify({
        "ok": True,
        "result": {
            "access-token": session_token
        }
    })
