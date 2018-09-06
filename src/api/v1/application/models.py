from . import db

class User(db.Document):
    id = db.StringField()
    username = db.StringField()
    email = db.StringField()
    password = db.BinaryField()
    balance = db.IntegerField()
    status = db.StringField()
