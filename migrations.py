import sqlite3


def connect(database):
    return sqlite3.connect(database)


def users(conn: sqlite3.Connection):
    conn.cursor().execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            email VARCHAR UNIQUE,
            password VARCHAR,
            service_user_id INT
        )
    """)
