from . import db

class User(db.Document):
    id = db.StringField()
    username = db.StringField()
    email = db.StringField()
    password = db.BinaryField()
    balance = db.IntField()
    status = db.StringField()
    whitelist = db.ListField(db.StringField())

class Session(db.Document):
    id = db.StringField()
    token = db.StringField()
