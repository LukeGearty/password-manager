import sqlite3
from passwords import *

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


def register_user(username, password):
    con = get_db_connection()
    cur = con.cursor()

    if is_valid_master_password(password): # from passwords.py
        try:
            hashed_password = hash_password(password)
            cur.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username,hashed_password))
            con.commit()
            print("User registered successfully")
        except sqlite3.IntegrityError:
            print("Username already exists")
        finally:
            con.close()

    else:
        return False


def login_user(username, password):
    con = get_db_connection()
    cur = con.cursor()

    cur.execute('SELECT password FROM users WHERE username = ?', (username,))
    result = cur.fetchone()
    con.close()

    if result and check_password(password, result[0]):
        print('Login Successful')
        return True
    else:
        print("Invalid username")
        return False


def get_password(website_name):
    con = get_db_connection()
    cur = con.cursor()

    cur.execute("SELECT password FROM passwords WHERE website_name = ?", (website_name,))
    password = cur.fetchone()

    con.close()
    return password
