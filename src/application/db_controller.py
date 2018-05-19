from . import app
import os
import sqlite3 as sql
from hashlib import sha512
import string, random
from datetime import datetime

connection = sql.connect(app.config["DATABASE_PATH"], check_same_thread=False)
cursor = connection.cursor()

def hashTok(tok):
    return sha512(tok.encode()).hexdigest()

def getHashedPassword(id):
    cursor.execute("SELECT * FROM credentials WHERE id = ?", (id,))
    return cursor.fetchone()[1]

def getBalance(id):
    cursor.execute("SELECT * FROM balances WHERE id = ?", (id,))
    return cursor.fetchone()[1]

def createUser(id, password):
    hashed_password = hashTok(password)
    cursor.execute("INSERT INTO credentials ('id', 'passoword') VALUES (?, ?)", (id, hashed_password))
    cursor.execute("INSERT INTO balances ('id', 'quantity') VALUES (?, 0)", (id,))
    connection.commit()

def createToken(size=32, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def createSession(id):
    token = createToken()
    now = datetime.now().strftime("%y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO sessions ('token', 'date', 'id') VALUES (?, ?, ?)", (id, now, token))
    return id, now, token
