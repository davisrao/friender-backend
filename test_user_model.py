"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User
from flask_bcrypt import Bcrypt
# from sqlalchemy import exc


# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///friender_test"

# Now we can import app

from app import app

bcrypt = Bcrypt()

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

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


        db.session.add(test_u1)
        db.session.add(test_u2)

        db.session.commit()
    
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

    # def test_repr_method(self):
    #     """does the repr method work?"""

    #     test_user = User.query.get(self.test_u1_id)
        
    #     self.assertEqual(test_user.__repr__(), f"<User #{test_user.id}: {test_user.username}, {test_user.email}>")


    def test_user_signup(self):
        """Does signup return the correct user"""

        test_user_sign_up = User.signup("u", "u_firstName", "u_lastName", "u@utest.com", "u_hobbies", "u_interests", "12345", "u.png","password")
        # test_user_sign_up_2 = User.signup("Davis", "test1@test.com", "testing123", "/static/images/pic.png")

        # db.session.commit()

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

    # def test_serialize(self):
    #     """Does signup return the correct user"""

    #     test_user_serialize = User.serialize({'username':"u", 'first_name':"u_firstName", 'last_name':"u_lastName", 'email':"u@utest.com", 'hobbies':"u_hobbies", 'interests':"u_interests", 'zip_code':"12345", 'image':"u.png",'password':"password"})
    #     # test_user_sign_up_2 = User.signup("Davis", "test1@test.com", "testing123", "/static/images/pic.png")

    #     # db.session.commit()

    #     #tests successful username entered
    #     self.assertEqual(test_user_serialize, {
    #         'username':"u", 'first_name':"u_firstName", 'last_name':"u_lastName", 'email':"u@utest.com", 'hobbies':"u_hobbies", 'interests':"u_interests", 'zip_code':"12345", 'image':"u.png",'password':"password"
    #     })




#TODO: Test unhappy paths, test serialize

    # def test_unsuccessful_email_signup(self):
    #     """testing if error raises on blank email"""
    #     test_user_sign_up = User.signup("Jeanne", None, "testing123", None)

    #     db.session.add(test_user_sign_up)

    #     with self.assertRaises(exc.IntegrityError):
    #         db.session.commit()

    # def test_unsuccessful_username_signup(self):
    #     """testing if error raises on blank UN"""
    #     test_user_sign_up = User.signup(None, "test123@test.com", "testing123", None)

    #     db.session.add(test_user_sign_up)

    #     with self.assertRaises(exc.IntegrityError):
    #         db.session.commit()
    
    # def test_unsuccessful_password_signup(self):
    #     """testing if error raises on blank password"""

    #     with self.assertRaises(ValueError):
    #         User.signup("Jeanne", "test1234@test.com", None , None)

    # def test_successful_follow(self):
    #     """does is following detect succeesful follow
    #     does is following know when somebody is not following
    #     does is followed by detect both successful followed by and not followed by"""

    #     user_1 = User.query.get(self.test_u1_id)
    #     user_2 = User.query.get(self.test_u2_id)

    #     user_1.following.append(user_2)

    #     db.session.commit()

    #     # tests if user_1 is following user_2 and if user_2 is followed by user_1
    #     self.assertTrue(user_1.is_following(user_2))
    #     self.assertTrue(user_2.is_followed_by(user_1))

    #     # tests to make sure that user_2 is not following user_1 and user_2 is not following user_1
    #     # since we set it up that way
    #     self.assertFalse(user_2.is_following(user_1))
    #     self.assertFalse(user_1.is_followed_by(user_2))


    # def test_successful_authentication(self):
    #     """checks to see if user is successfully authenticated with correct UN and PW"""


    #     user_4 = User.signup(
    #             username="my_user",
    #             password="test_my_user",
    #             email="email@testuser.com",
    #             image_url=User.image_url.default.arg,
    #         )

    #     db.session.commit()

    #     self.assertTrue(user_4.authenticate(user_4.username,"test_my_user"))

    # def test_failed_password_authentication(self):
    #     """checks to see if user is NOT authenticated with incorrect PW"""
    #     user_1 = User.query.get(self.test_u1_id)

    #     with self.assertRaises(ValueError):
    #         user_1.authenticate(user_1.username,"12345")

    # def test_failed_username_authentication(self):
    #     """checks to see if user is NOT authenticated with incorrect UN"""
    #     user_1 = User.query.get(self.test_u1_id)

    #     self.assertFalse(user_1.authenticate("123","pass1"))

