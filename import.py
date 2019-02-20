import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine=create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))





#import books to the database from books.csv

def main():
    doc = open("books.csv")
    reader = csv.reader(doc)
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
        {"isbn": isbn, "title": title, "author": author, "year": year})
        print(f"Added book isbn {isbn} title {title} by {author} year: {year}")
    db.commit()

if __name__ == "__main__":
    main()








K9PPwrOh1HaznOBfZnbg

import requests
res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "K9PPwrOh1HaznOBfZnbg", "isbns": "9780060995065"})
print(res.json())


import requests
res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "K9PPwrOh1HaznOBfZnbg", "isbns": "074349671X"})
print(res.json())
