from . import DATABASE_PATH
import os
import sqlite3 as sql
from hashlib import sha512
import string, random
from datetime import datetime

connection = sql.connect(DATABASE_PATH, check_same_thread=False)
cursor = connection.cursor()

def hashTok(tok):
    return sha512(tok.encode()).hexdigest()

def getHashedPassword(id):
    cursor.execute("SELECT * FROM credentials WHERE id = ?", (id,))
    return cursor.fetchone()[1]

def getBalance(id):
    cursor.execute("SELECT * FROM balances WHERE 'id' = ?", (id,))
    result = cursor.fetchall()
    print("Balance:", result) # DEBUG: SHOW ALL ROWS
    return result[0][1]

def addBalance(id, quantity):
    balance = getBalance(id)
    new_balance = int(balance) + quantity
    cursor.execute("UPDATE balances SET quantity = ? WHERE id = ?", (new_balance, id))
    connecton.commit()

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
    cursor.execute("INSERT INTO sessions ('token', 'date', 'id') VALUES (?, ?, ?)", (token, now, id))
    connection.commit()
    return id, now, token

def getSessionID(token):
    cursor.execute("SELECT 'id' FROM sessions WHERE token = ?", (token,))
    match = cursor.fetchone()
    return match[0]

def sendMoney(from_id, to_id, quantity):
    from_balance = getBalance(from_id)
    to_balance = getBalance(to_id)
    if int(quantity) > from_balance:
        return 2
    if int(qunatity) <= 0:
        return 3
    addBalance(from_id, -quantity)
    addBalance(to_id, quantity)
    return 1
