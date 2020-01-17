import sqlite3

connection = sqlite3.connect("data.db")

cursor = connection.cursor()

cursor.execute("CREATE TABLE users(username text primary key, password text, time text)")

cursor.execute("CREATE TABLE ideas(user text, ideaname text, ideatext text, ideatime text primary key)")

connection.commit()
connection.close()
