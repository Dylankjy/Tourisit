import models.Validation as validation

from datetime import datetime

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, IntegerField, TextAreaField, FloatField
from wtforms.validators import InputRequired, Length, NumberRange


class ListingForm(FlaskForm):
    tour_name = StringField('tour_name', validators=[InputRequired(), Length(min=1, max=30,
                                                                             message='Name can only be 30 characters long!')])
    tour_brief = StringField('tour_brief', validators=[InputRequired(), Length(min=1, max=100,
                                                                               message='Brief description can only be 100 characters long!')])
    tour_desc = TextAreaField('tour_desc', validators=[InputRequired()])
    # render_kw will pass in a dictionary.. if you want to render custom css etc..
    # tour_desc = TextAreaField('tour_desc', validators=[InputRequired()], render_kw={"rows": 70, "cols": 11})
    # Only allow image files
    tour_img = FileField('tour_img', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Only Images are allowed!')])
    tour_price = FloatField('tour_price', validators=[InputRequired(), NumberRange(min=0, max=None,
                                                                                   message='Price cannot be below $0!')])


class Listing:
    def __init__(
            self,
            tour_name,
            tour_brief,
            tour_desc,
            tour_price,
            tg_uid,
            tour_img=''
    ):

        self.__tour_name = ''
        self.set_tour_name(tour_name)

        self.__tour_brief = ''
        self.set_tour_brief(tour_brief)

        self.__tour_desc = ''
        self.set_tour_desc(tour_desc)

        self.__tour_itinerary = []
        self.__tour_location = []
        self.__tour_price = 0
        self.set_tour_price(tour_price)

        self.__tour_img = ''
        self.set_tour_img(tour_img)

        self.__date_created = datetime.now()
        self.__tour_rating = 0
        self.__tour_review = []
        self.set_tg_uid(tg_uid)

    def set_tour_name(self, tour_name):
        try:
            assert len(tour_name) <= 30
        except AssertionError:
            print(f"{tour_name} must be less than {30} characters!")
        else:
            self.__tour_name = tour_name

    def set_tour_brief(self, tour_brief):
        try:
            assert len(tour_brief) <= 100
        except AssertionError:
            print(f"Brief Tour Description must be less than 100 characters!")
        else:
            self.__tour_brief = tour_brief

    def set_tour_desc(self, tour_desc):
        self.__tour_desc = tour_desc

    def add_tour_itinerary(self, itinerary):
        try:
            assert type(itinerary) == str
        except AssertionError:
            print(f"{itinerary} must be of type {str}")
        else:
            self.__tour_review.append(itinerary)

    def set_tour_location(self, tour_location):
        try:
            assert type(tour_location) == list
        except AssertionError:
            print(f"{tour_location} must be of type {list}")
        else:
            self.__tour_location.append(tour_location)

    def set_tour_price(self, tour_price):
        try:
            tour_price = float(tour_price)
        except ValueError:
            print(f"{tour_price} must be of type {float}")
        else:
            self.__tour_price = tour_price

    def set_tour_img(self, tour_img):
        self.__tour_img = tour_img

    def set_tour_rating(self, tour_rating):
        try:
            tour_rating = float(tour_rating)
        except ValueError:
            print(f"{tour_rating} must be of type {float}")
        else:
            self.__tour_rating = tour_rating

    def set_tour_review(self, tour_review):
        try:
            assert type(tour_review) == list
        except AssertionError:
            print(f"{tour_review} must be of type {list}")
        else:
            self.__tour_review.append(tour_review)

    def set_tg_uid(self, tg_uid):
        self.__tg_uid = tg_uid

    def return_obj(self):
        return {
            "tour_name": self.__tour_name,
            "tour_brief": self.__tour_brief,
            "tour_desc": self.__tour_desc,
            "tour_itinerary": self.__tour_itinerary,
            "tour_location": self.__tour_location,
            "tour_price": self.__tour_price,
            "tour_img": self.__tour_img,
            "date_created": self.__date_created,
            "tour_rating": self.__tour_rating,
            "tour_review": self.__tour_review,
            "tg_uid": self.__tg_uid,
        }
