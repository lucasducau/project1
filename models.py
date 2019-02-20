

#project description required to use raw sql when executing queries

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from SQLAlchemy import UniqueConstraint

db = SQLAlchemy()

class Books(db.Model):
    __tablename__ = "books"
    isbn = db.Column(db.String, primary_key=True, nullable=False, unique=True)
    title = db.Column(db.String nullable=False)
    author = db.Column(db.String nullable=False)
    year = db.Column(db.Integer nullable=False)


class Reviews(db.Model):
    __tablename__= "reviews"
