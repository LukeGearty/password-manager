from flask import Flask, render_template, request, flash, redirect, url_for
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
    if request.method == "GET":
        return render_template('login.html', name='login') 

if __name__=="__main__":
    create_db() # from db.py
    port = 5000
    app.run(host="0.0.0.0", port=port, debug=True)