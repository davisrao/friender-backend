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

    @classmethod
    def serialize(cls, self):
        """Serialize to dictionary"""
        return {
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "hobbies": self.hobbies,
            "interests": self.interests,
            "zip_code": self.zip_code,
            "image": self.image
        }

    @classmethod
    def signup(
            cls, 
            username,
            first_name,
            last_name,
            email,
            hobbies,
            interests,
            zip_code,
            image,
            password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            hobbies=hobbies,
            interests=interests,
            zip_code=zip_code,
            image=image,
            password=hashed_pwd,
        )

        db.session.add(user)
        db.session.commit()
        return user



def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """
    db.app = app
    db.init_app(app)