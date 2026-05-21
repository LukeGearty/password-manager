import sqlite3

"""

Requirements:
    Create a database for user with table for user and passwords
        user table:
            username
            password
        password table:
            website
            password - stored as an encrypted password

"""


DB = "passwords.db"


def create_db():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website_name TEXT NOT NULL,
            password TEXT NOT NULL
            )
    ''')

    con.commit()
    con.close()


# retrieval of password for a website
def get_db_connection():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row 
    con.execute("PRAGMA foreign_keys = ON")
    return con


def get_password(website_name):
    con = get_db_connection()
    cur = con.cursor()

    cur.execute("SELECT password FROM passwords WHERE website_name = ?", (website_name,))
    password = cur.fetchone()

    con.close()
    return password
