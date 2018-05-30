from . import DATABASE_PATH
import os
import sqlite3 as sql
from hashlib import sha512
import string
import random
import textwrap
from datetime import datetime

connection = sql.connect(DATABASE_PATH, check_same_thread=False)
cursor = connection.cursor()


def hashTok(tok, **kwargs):
    dig = sha512(tok.encode()).hexdigest()
    return dig


def getTime():
    return datetime.now().strftime("%y-%m-%d %H:%M:%S")


def getHashedPassword(id):
    cursor.execute("SELECT * FROM credentials WHERE id = ?", (id,))
    password = cursor.fetchone()[1]
    return password


def getBalance(id):
    cursor.execute("SELECT quantity FROM balances WHERE id = ?", (id,))
    result = []
    for r in cursor.fetchall():
        result.append(r)
    return result[0][0]


def addBalance(id, quantity):
    balance = getBalance(id)
    new_balance = int(balance) + quantity
    cursor.execute(
        "UPDATE balances SET quantity = ? WHERE id = ?", (new_balance, id))
    connection.commit()


def createUser(id, password):
    hashed_password = hashTok(password)
    cursor.execute(
        "INSERT INTO credentials ('id', 'passoword') VALUES (?, ?)", (id, hashed_password))
    cursor.execute(
        "INSERT INTO balances ('id', 'quantity') VALUES (?, 0)", (id,))
    connection.commit()


def createToken(size=32, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def createSession(id):
    token = createToken()
    now = datetime.now().strftime("%y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO sessions ('token', 'date', 'id') VALUES (?, ?, ?)", (token, now, id))
    connection.commit()
    return id, now, token


def getSessionID(token):
    cursor.execute("SELECT * FROM sessions WHERE token = ?", (token,))
    result = []
    for r in cursor.fetchall():
        result.append(r)
    return result[0][2]


def sendMoney(from_id, to_id, quantity):
    from_balance = getBalance(from_id)
    to_balance = getBalance(to_id)
    if int(quantity) > from_balance:
        return 2, 0
    if int(quantity) <= 0:
        return 3, 0
    addBalance(from_id, -quantity)
    addBalance(to_id, quantity)
    tr = addTransaction(from_id, to_id, quantity)
    return 1, tr


def addTransaction(from_id, to_id, q):
    now = getTime()
    unsigned = from_id + to_id + str(q) + now
    sign = hashTok(unsigned)
    query = "INSERT INTO transactions ('from', 'to', 'date', 'quantity', 'sign') VALUES (?, ?, ?, ?, ?)"
    cursor.execute(query, (from_id, to_id, now, q, sign))
    connection.commit()
    return sign, now, from_id, to_id, int(q)


def createRecv(from_id, time_exposed=600, max=1024, allow=[]):
    now = getTime()
    token = hashTok(from_id + str(time_exposed) + str(max) + now)
    cursor.execute(
        "INSERT INTO receive-token ('from', 'max-amount', 'allow', 'time-created', 'expires', 'token') VALUES (?, ?, ?, ?)",
        (from_id, int(max), json.dumps(allow), now, int(time_exposed), token)
    )
    connection.commit()
