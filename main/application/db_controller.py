import os
import sqlite3 as sql

connection = sql.connect(os.environ["DATABASE_PATH"], check_same_thread=False)
cursor = connection.cursor()
