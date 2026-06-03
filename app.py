from flask import Flask, render_template, request, flash, redirect, url_for, session
from db import *
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")


@app.route('/')
def index():
    return render_template('index.html', name="Password Manager")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        result = register_user(username, password) # from db

        if result:
            return redirect(url_for("login"))
        else:
            flash("Something went wrong in registering, please try again", "error")
            return redirect(url_for("register"))
    elif request.method == "GET":
        return render_template('register.html', name='register')



@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    try:
        if request.method == "GET":
            return render_template('login.html', name='login') 
        elif request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            if login_user(username, password):
                print("User logged in successfully")

                session["user"] = username

                return redirect(url_for("dashboard"))
            else:
                error = "Invalid username or password"
                flash("Invalid username or password", "error")
                return redirect(url_for("login"))
    except KeyError:
        return redirect(url_for("login"))


@app.route('/dashboard')
def dashboard():
    if "user" not in session:
        return redirect(url_for("index"))
    
    db_passwords = get_all_passwords()
    # get them into a dictionary where the key is website and value is the decrypted password

    passwords = {}

    for password in db_passwords:
        passwords[password[1]] = decrypt_password(password[2])
    # print(passwords)
    return render_template('dashboard.html', name="Dashboard", user=session["user"], passwords=passwords)


@app.route('/add_password', methods=["GET", "POST"])
def add_password():
    if request.method == "GET":
        return render_template('add_password.html', name="Add Password")
    elif request.method == "POST":
        # flow: create password -> encrypt password -> insert into database
        
        website_name = request.form["website"]
        password = create_password()

        encrypted_password = encrypt_password(password)

        insert_password(website_name, encrypted_password)
        print("Password entered successfully")
        return redirect(url_for("dashboard"))




if __name__=="__main__":
    create_db() # from db.py
    port = 5000
    app.run(host="0.0.0.0", port=port, debug=True)