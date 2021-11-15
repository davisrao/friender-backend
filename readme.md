# Overview
* Back end for a "tinder for friends" concept
* Currently, users can sign up / log in and see potential matches in their same zip code
* Likes or Passes are added to a db as an "action"

# Testing
* Testing exists on user model, but only for sign up and to ensure the overall user model works
* More testing needs to be added to ensure serialization is working properly, and that unhappy paths are covered
* to run existing user model tests:  python -m unittest test_user_model.py

# TODO: what would I like to do here with more time?
* Testing - build out more tests to improve coverage. User routes should be tested first
* Messaging - when you match with somebody, you should be able to shoot them a message
* Move AWS to its own file so we arent just doing in the app
* Better structure of files
* User editing + allow users to add multiple pictures
* Error handling for forms