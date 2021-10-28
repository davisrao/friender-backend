# from logging import debug
from werkzeug.utils import secure_filename
import os
import boto3

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



img = "./rithm.png"

s3 = boto3.client(
  "s3",
  "us-west-1",
  aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
  aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
)


filename = secure_filename(img)
# img.save(filename) // wasnt importing correctly testing without
s3.upload_file(
    Bucket = os.environ['BUCKET'],
    Filename=filename,
    Key = filename
)