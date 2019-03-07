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





@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        if session.get("logged_in"):

            flash('You are already logged in')
            return redirect(url_for('search'),"303")
        else:

            return render_template("index.html")

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        check = db.execute("SELECT username, password FROM users WHERE username = :username", {"username": username}).fetchone()

        if not check:
            flash('Invalid Username')
            return redirect(url_for('index'), '303')

        db_username = check.username
        db_hash = check.password

        flash(db_username)
        flash(db_hash)



#        db_hash = db_hash[0].encode("utf-8")
        if pbkdf2_sha256.verify(password, db_hash):
            session['logged_in'] = True
            session['user_id'] = db_username
            flash('Logged In')
            return redirect(url_for('search'), '303')

        else:
           flash('Invalid login')
           return redirect(url_for('index'), '303')



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


@app.route("/search", methods=["POST", "GET"])
def search():
    if request.method == "GET":
        return render_template('search.html')

    if request.method == "POST":

        type = request.form.get("searchtype")
        query = request.form.get("searchquery")

        results = db.execute("SELECT * FROM books WHERE title = :query", {"query": query}).fetchall()
        flash(type)
        flash(query)
        return render_template('search.html', results=results)


@app.route("/logout", methods=["GET"])
def logout():

    if session['logged_in'] == True:
        session['logged_in'] = False
        session['user_id'] = None
        flash('Logged out successfully')
        return redirect(url_for('index'))

    if session['logged_in'] == False:
        flash('You are not logged in')
        return redirect(url_for('index'))





@app.route("/error", methods=["GET"])
def error():
    errorMsg = "Welcome to the error page"
    return render_template('error.html', errorMsg=errorMsg)
