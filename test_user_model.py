"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User
from flask_bcrypt import Bcrypt
# from sqlalchemy import exc

# Setting env variable to use different DB for tests.
# need to do before the app is imported.

os.environ['DATABASE_URL'] = "postgresql:///friender_test"

# Now we can import app

from app import app

bcrypt = Bcrypt()

# Create our tables once
# after / before each we'll refresh the data inside

db.create_all()


class UserModelTestCase(TestCase):
    """Test for User Model."""

    def setUp(self):
        """Create test client, add sample data."""
        User.query.delete()

        self.client = app.test_client()

        test_u1 = User(
            username="u1_username",
            first_name="u1_firstName",
            last_name="u1_lastName",
            email="u1@test.com",
            hobbies="u1_hobbies",
            interests="u1_interests",
            zip_code="12345",
            image="u1_username.png",
            password="test123"
        )

        test_u2 = User(
            username="u2_username",
            first_name="u2_firstName",
            last_name="u2_lastName",
            email="u2@test.com",
            hobbies="u2_hobbies",
            interests="u2_interests",
            zip_code="12345",
            image="u2_username.png",
            password="test123"
        )


        #add and commit that to the db
        db.session.add(test_u1)
        db.session.add(test_u2)

        db.session.commit()

        #grabbing here as we are not sure what we are gonna get as ID because 
        # of auto incrementing primary key
        self.test_u1_id = test_u1.user_id
        self.test_u2_id = test_u2.user_id
    
    def tearDown(self):
        """Stuff to do after every test."""
        db.session.rollback()


    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            username="u_username",
            first_name="u_firstName",
            last_name="u_lastName",
            email="u@test.com",
            hobbies="u_hobbies",
            interests="u_interests",
            zip_code="12345",
            image="u_username.png",
            password="test123"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        totalUsers = User.query.all()
        self.assertEqual(len(totalUsers), 3)

    def test_repr_method(self):
        """does the repr method work?"""

        test_user = User.query.get(self.test_u1_id)

        self.assertEqual(test_user.__repr__(), f"<User #{self.test_u1_id}: {test_user.username}>")


    def test_user_signup(self):
        """Does signup return the correct user"""

        test_user_sign_up = User.signup("u", "u_firstName", "u_lastName", "u@utest.com", "u_hobbies", "u_interests", "12345", "u.png","password")

        #tests successful username entered
        self.assertEqual(test_user_sign_up.username, "u")

        #tests successful firstname entered
        self.assertEqual(test_user_sign_up.first_name, "u_firstName")
        #tests successful username entered
        self.assertEqual(test_user_sign_up.last_name, "u_lastName")

        #tests successful email entered
        self.assertEqual(test_user_sign_up.email, "u@utest.com")

        #tests successful hobbies
        self.assertEqual(test_user_sign_up.hobbies, "u_hobbies")

        #tests successful interests
        self.assertEqual(test_user_sign_up.interests, "u_interests")

        #tests successful zupcode
        self.assertEqual(test_user_sign_up.zip_code, "12345")

        #tests successful image
        self.assertEqual(test_user_sign_up.image, "u.png")

        #tests successful password hash
        self.assertTrue(bcrypt.check_password_hash(test_user_sign_up.password, "password"))


    def test_serialize(self):
        """Does serialize method on the class work"""
        user_queried=User.query.get(self.test_u1_id)
        test_user_serialize = User.serialize(user_queried)

        self.assertEqual(test_user_serialize['username'], "u1_username")
        self.assertEqual(test_user_serialize['hobbies'], "u1_hobbies")
        self.assertEqual(test_user_serialize['user_id'], self.test_u1_id)


    def test_successful_authentication(self):
        """checks to see if user is successfully authenticated with correct UN and PW"""
        u = User.signup(
            username="u_username",
            first_name="u_firstName",
            last_name="u_lastName",
            email="u@test.com",
            hobbies="u_hobbies",
            interests="u_interests",
            zip_code="12345",
            image="u_username.png",
            password="test123"
        )
        db.session.add(u)
        db.session.commit()
        self.assertTrue(u.authenticate(u.username,"test123"))

    def test_failed_password_authentication(self):
        """checks to see if user is NOT authenticated with incorrect PW"""
        user_queried=User.query.get(self.test_u1_id)

        with self.assertRaises(ValueError):
            user_queried.authenticate(user_queried.username,"wrongpass")

    def test_failed_username_authentication(self):
        """checks to see if user is NOT authenticated with incorrect UN"""
        user_queried=User.query.get(self.test_u1_id)

        self.assertFalse(user_queried.authenticate("wrong","test123"))

#TODO: Test unhappy paths for sign up