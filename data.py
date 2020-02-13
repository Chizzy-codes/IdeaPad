import sqlite3


def create_tables():
    connection = sqlite3.connect("data.db")

    cursor = connection.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY,  username text, password text, time text)")

    cursor.execute("CREATE TABLE IF NOT EXISTS ideas(id integer, ideaname text, ideatext text, ideatime text)")

    connection.commit()
    connection.close()
