"""SQLAlchemy models for Warbler."""

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import backref

bcrypt=Bcrypt()
db=SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    username = db.Column(
        db.Text,
        nullable=False,
        primary_key=True,
    )

    first_name = db.Column(
        db.Text,
        nullable=False,
    )

    last_name = db.Column(
        db.Text,
        nullable=False,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    hobbies = db.Column(
        db.Text,
        nullable=True,
    )

    interests = db.Column(
        db.Text,
        nullable=True,
    )

    zip_code = db.Column(
        db.VARCHAR(5),
        nullable=False,
    )

    #TODO: create friend radius table
    #TODO: default image for image

    image = db.Column(
        db.Text,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """
    db.app = app
    db.init_app(app)