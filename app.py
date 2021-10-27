from logging import debug
from werkzeug.utils import secure_filename
import os

from flask import Flask, jsonify, request, flash, redirect, session, g
# from flask_debugtoolbar import DebugToolbarExtension
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError

# from forms import CSRFOnlyForm, EditUserForm, UserAddForm, LoginForm, MessageForm
from models import db, connect_db, User

import dotenv
dotenv.load_dotenv()

CURR_USER_KEY = "curr_user"

app = Flask(__name__)
import boto3

bcrypt= Bcrypt()

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ['DATABASE_URL'].replace("postgres://", "postgresql://"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
# toolbar = DebugToolbarExtension(app)

connect_db(app)

s3 = boto3.client(
  "s3",
  "us-west-1",
  aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
  aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
)

##############################################################################
# User Routes
@app.get('/users')
def list_users():
    """Returns JSON list of all user dictionaries.
        {users:[{user1},...]}
    """

    users = User.query.all()
    breakpoint()
    serialized = [User.serialize(user) for user in users]

    return jsonify(users=serialized)

@app.route('/users', methods=["GET","POST"])
def create_user():
    """Takes is user info as dictionary,
    Adds a new user to the database, and returns added user object.
        {
            "username",
            "first_name",
            "last_name",
            "email",
            "hobbies",
            "interests",
            "zip_code",
            "image"         
        }
    """
    # breakpoint()
    #FIXME: While importing 'app', an ImportError was raised. due to boto3 import
    img = request.files['file']
    if img:
        filename = secure_filename(img.filename)
        # img.save(filename)
        s3.upload_file(
            Bucket = os.environ['BUCKET'],
            Filename=filename,
            Key = filename
        )

    user = User.signup(
        
            username=request.json["username"],
            first_name=request.json["first_name"],
            last_name=request.json["last_name"],
            email=request.json["email"],
            hobbies=request.json["hobbies"],
            interests=request.json["interests"],
            zip_code=request.json["zip_code"],
            image=filename,
            password=request.json["password"],
        )
    serialized = User.serialize(user)

    return jsonify(user=serialized)

    """
    1. function to call the sigup route passing in the form data
    2. Then form data is in the route
    """