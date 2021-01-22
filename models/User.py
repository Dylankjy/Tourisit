from datetime import datetime

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, PasswordField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo

import auth as auth
from models.Format import file_to_base64

def fb_check(form, field):
    if 'facebook.com' not in field.data:
        raise ValidationError('Invalid Facebook Profile link')

def insta_check(form, field):
    if 'instagram.com' not in field.data:
        raise ValidationError('Invalid Instagram Profile link')

def linkedin_check(form, field):
    if 'linkedin.com' not in field.data:
        raise ValidationError('Invalid LinkedIn Profile link')

def password_check(form, field):
    result = auth.is_auth(True, True)
    if result:
        checker = auth.check_password_correlate(field.data, result['password'])
        if not checker:
            raise ValidationError('Wrong password entered!')
    else:
        return False

class PasswordForm(FlaskForm):
    old_password = PasswordField(
        'old_password',
        validators=[
            InputRequired(),
            password_check
        ]
    )

    password = PasswordField(
        'New Password',
        validators=[
            InputRequired(),
            EqualTo('confirm', message='Passwords must match')
        ]
    )
    confirm = PasswordField('Repeat Password')

class UserForm(FlaskForm):
    name = StringField(
        "name",
        validators=[
            InputRequired(),
            Length(min=1, max=30, message="Testing")]
    )
    pfp_img = FileField(
        'pfp_img',
        validators=[
            FileAllowed(['jpg', 'jpeg', 'png'], 'Only .jpg, .jpeg and .png images are allowed!')]
    )
    email = StringField(
        "email",
        validators=[
            InputRequired(),
            Length(
                min=1,
                max=30,
                message="Email can only be 30 characters long!"),
        ],
    )
    phone_number = StringField(
        "phone_number",
        validators=[
            InputRequired(),
            Length(min=8, max=8, message="Phone number can only be 8 long"),
        ],
    )
    fb = StringField(
        "fb",
        validators=[
            Length(max=200, message='Input a valid Facebook link!'),
            fb_check
        ],
    )
    insta = StringField(
        "insta",
        validators=[
            Length(max=200, message="Input a valid Instagram link!"),
            insta_check
        ],
    )
    linkedin = StringField(
        "linkedin",
        validators=[
            Length(max=200, message="Input a valid Instagram link!"),
            linkedin_check
        ],
    )
    account_mode = SelectField(
        "account_mode",
        choices=[(0, 'Tourist'), (1, 'Tour Guide')],
        validators=[
            InputRequired()
        ],
    )

class BioForm(FlaskForm):
    bio = TextAreaField(
        "bio",
        validators=[
            Length(min=0, max=75, message="Bio can only be 75 characters long!")
        ]
    )

class User:
    def __init__(
            self,
            name,
            password,
            email,
            phone_number="",
            bio="",
            profile_img=file_to_base64('public/imgs/uwu.png'),
            last_seen_time="",
            registration_time="",
            stripe_ID="",
            wishlist=[],
            fb="",
            insta="",
            linkedin="",
            socialmedia={},
            email_status=False,
            phone_status=False,
            account_type=0,
            account_mode=-1,
            verified=0
    ):
        self.__name = ""
        self.set_name(name)

        self.__password = ""
        self.set_password(password)

        self.__email = ""
        self.set_email(email.lower())

        self.__phone_number = ""
        self.set_phone_number(phone_number)

        self.__bio = ""
        self.set_bio(bio)

        self.__profile_img = ''
        self.set_profile_img(profile_img)

        self.__last_seen_time = last_seen_time
        self.__registration_time = registration_time
        self.__stripe_ID = stripe_ID
        self.__wishlist = wishlist

        self.__fb = ""
        self.set_fb(fb)

        self.__insta = ""
        self.set_insta(insta)

        self.__linkedin = ""
        self.set_linkedin(linkedin)

        self.__socialmedia = {}
        self.set_socialmedia(socialmedia, fb, insta, linkedin)

        self.__email_status = False
        self.set_email_status(email_status)

        self.__phone_status = False
        self.set_phone_status(phone_status)

        self.__account_type = account_type

        # -1 = new account
        # 0 = tourist
        # 1 = tour guide
        self.__account_mode = account_mode
        self.__verified = verified
        # Generate timestamp in ISO format
        date = datetime.now()
        current_timestamp = date.isoformat()

        self.__registration_time = current_timestamp

    def set_name(self, name):
        self.__name = name

    def set_password(self, password):
        self.__password = password

    def set_email(self, email):
        self.__email = email

    def set_phone_number(self, phone_number):
        self.__phone_number = phone_number

    def set_bio(self, bio):
        self.__bio = bio

    def set_socialmedia(self, socialmedia, fb, insta, linkedin):
        self.__socialmedia.update({"fb": fb})
        self.__socialmedia.update({"insta": insta})
        self.__socialmedia.update({"linkedin": linkedin})
        self.__socialmedia = socialmedia

    def set_fb(self, fb):
        self.__fb = fb

    def set_insta(self, insta):
        self.__insta = insta

    def set_linkedin(self, linkedin):
        self.__linkedin = linkedin

    def set_email_status(self, email_status):
        self.__email_status = email_status

    def set_phone_status(self, phone_status):
        self.__phone_status = phone_status

    def set_profile_img(self, profile_img):
        self.__profile_img = profile_img

    def return_obj(self):
        return {
            "name": self.__name,
            "password": self.__password,
            "email": self.__email,
            "phone_number": self.__phone_number,
            "bio": self.__bio,
            "profile_img": self.__profile_img,
            "last_seen_time": self.__last_seen_time,
            "registration_time": self.__registration_time,
            "stripe_id": self.__stripe_ID,
            "wishlist": self.__wishlist,
            "socialmedia": {
                "fb": self.__fb,
                "insta": self.__insta,
                "linkedin": self.__linkedin,
            },
            "email_status": self.__email_status,
            "phone_status": self.__phone_status,
            "account_type": self.__account_type,
            "account_mode": self.__account_mode,
            "verified": self.__verified
        }
