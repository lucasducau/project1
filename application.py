import os
import datetime
import requests

from flask import Flask, session, render_template, request, redirect, url_for, jsonify
from flask import flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from passlib.hash import pbkdf2_sha256





now = datetime.datetime.now()
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


        query = request.form.get("searchquery")
        try:
            yeartext = int(query)
        except ValueError:
            yeartext = 0

        text = f"%{query}%".lower()



        results = db.execute("SELECT * FROM books WHERE LOWER(title) LIKE :title OR LOWER(author) LIKE :author OR year = :year OR LOWER(isbn) LIKE :isbn"
        ,{"title": text, "author": text, "year": yeartext, "isbn": text}).fetchall()


        if len(results) == 0:
            flash('No results found')
            return render_template('search.html')


    #    flash(query)
    #    flash(text)
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


@app.route("/book/<string:isbn>", methods=["GET","POST"])
def book(isbn):
    if request.method == "GET":
        goodreadsRequest = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "K9PPwrOh1HaznOBfZnbg", "isbns": isbn})
        goodreads = goodreadsRequest.json()
        book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
        if book is None:
            return render_template('error.html', errorMsg="Book not found.")

        reviews = db.execute("SELECT * FROM reviews WHERE isbn = :isbn ORDER BY dateandtime DESC", {"isbn": isbn}).fetchall()
        query = db.execute("SELECT * FROM users").fetchall()

        #the way stars are displayed in the html is awful i know but i can't make it work and want to move on to another project
        return render_template('book.html', book=book,reviews=reviews,goodreads=goodreads)

    if request.method == "POST":
        username = session['user_id']
        userquery = db.execute("SELECT user_id FROM users WHERE username = :username", {"username": username}).fetchone()
        user_id = userquery.user_id
        review = request.form.get("review")
        datetime = now.strftime("%Y-%m-%d %H:%M:%S")
        current_book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn":isbn}).fetchone()
        star_number = int(request.form.get("star_number"))
        if not db.execute("SELECT * FROM reviews WHERE isbn = :isbn AND user_id = :id", {"isbn": isbn,"id": user_id}).rowcount == 0:
            return render_template('error.html', errorMsg="You have already submitted a review for this book")

        db.execute("INSERT INTO reviews (dateandtime, isbn, user_id, review_text, username, star_number) VALUES (:dateandtime,:isbn,:user_id,:review_text, :username, :star_number)",
        {"dateandtime": datetime,"isbn": current_book.isbn, "user_id": user_id, "review_text": review, "username": username, "star_number": star_number})
        db.commit()

        return redirect(url_for('book', isbn=current_book.isbn))





@app.route("/error", methods=["GET"])
def error():
    errorMsg = "Welcome to the error page"
    return render_template('error.html', errorMsg=errorMsg)


@app.route("/api/book/<string:isbn>")
def api(isbn):
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    reviews = db.execute("SELECT * FROM reviews WHERE isbn = :isbn", {"isbn": isbn}).fetchall()
    if book is None:
        return jsonify({
            "error_code": 404,
            "error_message": "Book not found"

            }), 404

    json = {"title": book.title,
            "author": book.author,
            "year": book.year,
            "isbn": book.isbn,
            "number_of_reviews": len(reviews)
            }

    return jsonify(json)
