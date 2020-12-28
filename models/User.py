from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Length


class UserForm(FlaskForm):
    name = StringField(
        "name",
        validators=[
            InputRequired(),
            Length(min=1, max=30, message="Testing")]
    )
    password = StringField(
        "password",
        validators=[
            InputRequired()
        ],
    )
    email = StringField(
        "email",
        validators=[
            InputRequired(),
            Length(min=1, max=30, message="Email can only be 30 characters long!"),
        ],
    )
    phone_number = StringField(
        "phone_number",
        validators=[
            InputRequired(),
            Length(min=8, max=8, message="Phone number can only be 8 long"),
        ],
    )


class User:
    def __init__(
            self,
            name,
            password,
            email,
            phone_number,
            bio="",
            profile_img="",
            last_seen="",
            last_activity="",
            stripe_ID="",
            wishlist=[],
            fb="",
            insta="",
            linkedin="",
    ):
        self.__name = ""
        self.set_name(name)

        self.__password = ""
        self.set_password(password)

        self.__email = ""
        self.set_email(email)

        self.__phone_number = ""
        self.set_phone_number(phone_number)

        self.__bio = bio
        self.__profile_img = profile_img
        self.__last_seen = last_seen
        self.__last_activity = last_activity
        self.__stripe_ID = stripe_ID
        self.__wishlist = wishlist
        self.__fb = fb
        self.__insta = insta
        self.__linkedin = linkedin

    def set_name(self, name):
        try:
            assert len(name) <= 30
        except AssertionError:
            print(f"{name} must be less than {30} characters!")
        else:
            self.__name = name

    def set_password(self, password):
        self.__password = password

    def set_email(self, email):
        self.__email = email

    def set_phone_number(self, phone_number):
        try:
            assert len(phone_number) == 8
        except AssertionError:
            print(f"{phone_number} must be less than {8} numbers!")
        else:
            self.__phone_number = phone_number

    def set_bio(self, bio):
        try:
            assert len(bio) <= 50
        except AssertionError:
            print(f"{bio} must be less than {50} characters!")
        else:
            self.__bio = bio

    def return_obj(self):
        return {
            "name": self.__name,
            "password": self.__password,
            "email": self.__email,
            "phone_number": self.__phone_number,
            "bio": self.__bio,
            "profile_img": self.__profile_img,
            "last_seen": self.__last_seen,
            "last_activity": self.__last_activity,
            "stripe_id": self.__stripe_ID,
            "wishlist": self.__wishlist,
            "socialmedia": {
                "fb": self.__fb,
                "insta": self.__insta,
                "linkedin": self.__linkedin,
            },
        }
