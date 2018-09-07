from . import bcrypt, mail, serializer
from .models import User, Session
from time import time
from random import randint
from flask import Blueprint, request, abort, render_template, jsonify
from flask_mail import Message

auth = Blueprint("authorization", __name__)

@auth.route("/register", methods=["POST"])
def registerUser():
    ip = request.remote_addr
    payload = request.get_json()
    required = ["password", "email", "username"]

    if not set(payload) >= set(required):
        return abort(400)

    password = payload["password"]
    email = payload["email"]
    username = payload["username"]

    if User.query.filter_by(email=email).first() is not None:
        return abort(409)

    def generateID():
        temp = randint(0, 999999999999)

        if User.query.filter_by(id=str(temp)).first() is not None:
            generateID()
        
        return str(temp)

    id = generateID()

    user = User(
        id = id,
        password = bcrypt.generate_password_hash(password),
        email = email,
        username = username,
        balance = 0,
        status = "unverified",
        whitelist = [ip]
    )

    user.save()

    msg = Message(
        "Verify your Account",
        recipients=[email]
    )

    token = serializer.dumps(email, salt="verify-account")

    msg.html = render_template("emails/verify.html", username=username, token=token)

    mail.send(msg)

    return jsonify({
        "ok": True,
        "result": {
            "id": id,
            "description": "Check your Inbox to verify this account."
        }
    })

@auth.route("/login", methods=["POST"])
def loginUser():
    payload = request.get_json()
    required = ["id", "password", "remove-previous-sessions"]
    ip = request.remote_addr

    if not set(required) >= set(payload):
        return abort(400)

    id = payload["id"]
    password = payload["password"]
    remove = payload["remove-previous-sessions"]

    user = User.query.filter_by(id=id).first()

    if user is None:
        abort(404)

    print(user)

    if not bcrypt.check_password_hash(user.password, password):
        return abort(401)
    
    if user.status == "unverified":
        return abort(401)

    existing = Session.query.filter_by(id=id)

    if remove:
        for s in existing:
            s.remove()

    session_token = serializer.dumps(user.id + str(time()), salt="session-token")[:32]

    session = Session(id=user.id, token=session_token)

    session.save()

    if ip not in user.whitelist:
        msg = Message(
            "New Access from a New location",
            recipients=[user.email]
        )

        msg.html = render_template("emails/access.html", username=user.username, id=user.id, ip=ip)

        mail.send(msg)

        return jsonify({
            "ok": True,
            "result": {
                "description": "Check your Inbox to whitelist this IP."
            }
        })

    msg = Message(
        "New Access from your Account",
        recipients=[user.email]
    )

    msg.html = render_template("emails/new.html", username=user.username, id=user.id, ip=ip)

    mail.send(msg)

    return jsonify({
        "ok": True,
        "result": {
            "access-token": session_token
        }
    })
