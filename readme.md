# Overview
* Back end for a "tinder for friends" concept
* Currently, users can sign up / log in and see potential matches in their same zip code
* Likes or Passes are added to a db as an "action"

# Testing
* Testing exists on user model, but only for sign up and to ensure the overall user model works
* More testing needs to be added to ensure serialization is working properly, and that unhappy paths are covered
* to run existing user model tests:  python -m unittest test_user_model.py

# Installing the stack:
* Python: MacOS comes with python installed but it is an old version. To use homebrew to install latest: brew install python
* Database: install postgres with homebrew -- brew install postgresql@13
* Start postgres: brew services start postgresql

# INSTALLING DEPENDENCIES:
* initialize a venv within project directory -- python -m venv venv
* activate venv -- source venv/bin/activate
* install requirements. pip install -r requirements.txt
* create database in cmd line: createdb friender
* create test database in cmd line (test files will connect to this DB but .env needs to be created as well per last step here): createdb friender_test
* run seed.py with python to create latest db tables from models file (ensure this happened with PSQL)
* create .env file with following variables SECRET_KEY, ACCESS_KEY, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, DATABASE_URL, BUCKET, JWT_SECRET_KEY. 
* create gitignore file with __pycache__, .env, and /venv

# TODO: what would I like to do here with more time?
* Biggest thing is ensuring the g is used in flask - when there is a login, we need to say add this user to flask g and then ensure login on each subsequent check.
* Testing - build out more tests to improve coverage. Add tests to react app + routes for users etc. 
* Log out btn :)
* Move AWS to its own file so we arent just doing in the app
* Messaging - when you match with somebody, you should be able to shoot them a message
* Better structure of files
* User editing + allow users to add multiple pictures
* Error handling for forms