"""SQLAlchemy models for Warbler."""



from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


bcrypt=Bcrypt()
db=SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(
        db.Integer,
        primary_key=True,
    )
    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
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
            "user_id": self.user_id,
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
        # print (user.user_id)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Action(db.Model):
    __tablename__ = 'actions'

    acting_user_id= db.Column(
        db.Integer,
        db.ForeignKey('users.user_id', ondelete="cascade"),
        primary_key=True,
    )
    targeted_user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.user_id', ondelete="cascade"),
        primary_key=True,
    )

    action = db.Column(
        db.Text,
        nullable=False,
    )
    @classmethod
    def add(cls,
            acting_user_id, targeted_user_id,action):
        """add action to db.
        """
        action=Action(acting_user_id=acting_user_id, 
                        targeted_user_id=targeted_user_id,
                        action=action)

        db.session.add(action)
        db.session.commit()

        return action

    @classmethod
    def serialize(cls, self):
        """Serialize to dictionary"""
        return {
            "acting_user_id": self.acting_user_id,
            "targeted_user_id": self.targeted_user_id,
            "action": self.action,
        }

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """
    db.app = app
    db.init_app(app)