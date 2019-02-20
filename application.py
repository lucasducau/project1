import os

from flask import Flask, session, render_template, request, redirect, url_for, jsonify
from flask import flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from passlib.hash import pbkdf2_sha256


app = Flask(__name__)
app.secret_key = "eNdOrJe"



# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == "GET":
        if session.get("logged_in"):
            flash('You are already logged in')
            return redirect(url_for('index'),"303")
        else:
            return render_template("register.html")
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        password2 = request.form.get("password2")

        if password != password2 or password is None or password2 is None:
            flash("Passwords don't match")
            return redirect(url_for('register'), "303")

        hash = pbkdf2_sha256.hash(password)


        if not db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).rowcount == 0:
            flash('Username already taken')
            return redirect(url_for('register'),'303')

        db.execute("INSERT INTO users (username,password) VALUES (:username, :hash)",
                    {"username": username, "hash": hash})

        db.commit()
        flash('Registration successful')
        return redirect(url_for('index'))
