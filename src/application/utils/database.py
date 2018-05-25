from . import DATABASE_PATH
import os
import sqlite3 as sql
from hashlib import sha512
import string, random
from datetime import datetime

def connectDatabase():
    connection = sql.connect(DATABASE_PATH, check_same_thread=False)
    cursor = connection.cursor()
    return connection, cursor

def hashTok(tok):
    return sha512(tok.encode()).hexdigest()

def getHashedPassword(id):
    connection, cursor = connectDatabase()
    cursor.execute("SELECT * FROM credentials WHERE id = ?", (id,))
    return cursor.fetchone()[1]
    connection.close()

def getBalance(id):
    connection, cursor = connectDatabase()
    cursor.execute("SELECT * FROM balances WHERE 'id' = ?", (id,))
    result = cursor.fetchone()
    print("Balance:", result) # DEBUG: SHOW ALL ROWS
    connection.close()
    return result[1]

def addBalance(id, quantity):
    connection, cursor = connectDatabase()
    balance = getBalance(id)
    new_balance = int(balance) + quantity
    cursor.execute("UPDATE balances SET quantity = ? WHERE id = ?", (new_balance, id))
    connection.commit()
    connection.close()

def createUser(id, password):
    connection, cursor = connectDatabase()
    hashed_password = hashTok(password)
    cursor.execute("INSERT INTO credentials ('id', 'passoword') VALUES (?, ?)", (id, hashed_password))
    cursor.execute("INSERT INTO balances ('id', 'quantity') VALUES (?, 0)", (id,))
    connection.commit()
    connection.close()

def createToken(size=32, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def createSession(id):
    connection, cursor = connectDatabase()
    token = createToken()
    now = datetime.now().strftime("%y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO sessions ('token', 'date', 'id') VALUES (?, ?, ?)", (token, now, id))
    connection.commit()
    connection.close()
    return id, now, token

def getSessionID(token):
    connection, cursor = connectDatabase()
    cursor.execute("SELECT 'id' FROM sessions WHERE token = ?", (token,))
    match = cursor.fetchone()
    connection.close()
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
