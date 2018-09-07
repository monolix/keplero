from . import bcrypt, mail, s
from .models import User, Session
from time import time
from random import randint
from flask import Blueprint, request, abort, render_template, jsonify
from flask_mail import Message

auth = Blueprint("authorization", __name__)

@auth.route("/register", methods=["POST"])
def registerUser():
    payload = request.get_json()
    required = ["password", "email", "username"]

    if not set(payload) >= set(required):
        return abort(400)

    password = payload["password"]
    email = payload["email"]
    username = payload["username"]

    if User.query.filter_by(email=email):
        return abort(409)

    def generateID():
        temp = randint(0, 999999999999)

        if User.query.filter_by(id=temp).first() is not None:
            generateID()
        
        return temp

    id = generateID()

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
            "id": id,
            "description": "Check your Inbox to verify this account."
        }
    })

@auth.route("/login", methods=["POST"])
def loginUser():
    payload = request.get_json()
    required = ["id", "password", "add"]
    ip = request["remote_addr"]

    if not set(required) >= set(payload):
        return abort(400)

    id = payload["id"]
    password = payload["password"]
    add = payload["add"]

    user = User.query.filter_by(id=id).first()

    if not bcrypt.check_password_hash(user.password, password):
        return abort(401)
    
    if user.status == "unverified":
        return abort(401)

    existing = Session.query.filter_by(id=id)

    if add == False:
        for s in existing:
            s.remove()

    session_token = s.dumps(user.id + str(time()), salt="session-token")[:32]

    session = Session(id=user.id, token=session_token)

    session.save()

    u = User.query.filter_by(id=id).first()

    if ip not in u.whitelist:
        msg = Message(
            "New Access from a New location",
            recipients=[u.email]
        )

        msg.html = render_template("emails/access.html", username=u.username, id=u.id, ip=ip)

        return jsonify({
            "ok": True,
            "result": {
                "description": "Check your Inbox to whitelist this IP."
            }
        })

    return jsonify({
        "ok": True,
        "result": {
            "access-token": session_token
        }
    })
