from datetime import datetime

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, FloatField, IntegerField, SelectField
from wtforms.validators import InputRequired, Length, NumberRange


# Add no. of revisions, itineary, location
class ListingForm(FlaskForm):
    tour_name = StringField('tour_name', validators=[InputRequired(), Length(min=1, max=30,
                                                                             message='Name can only be 30 characters long!')])

    tour_desc = TextAreaField('tour_desc', validators=[InputRequired()])

    #Tour itinerary
    tour_items = StringField('tour_items', validators=[InputRequired()])

    tour_loc = SelectField('tour_loc', choices=['Ang Mo Kio', 'Bedok', 'Bishan', 'Bukit Batok', 'Bukit Merah', 'Bukit Panjang', 'Bukit Timah',
                                                 'Choa Chu Kang', 'Clementi', 'Changi', 'Geylang', 'Hougang', 'Jurong East', 'Jurong West',
                                                'Kallang', 'Marine Parade', 'Orchard', 'Pasir Ris', 'Punggol', 'Queenstown', 'Sembawang', 'Sengkang',
                                                'Serangoon', 'Sentosa', 'Tampines', 'Toa Payoh', 'Woodlands', 'Yishun'])

    tour_img = FileField('tour_img', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Only Images are allowed!')])

    tour_revisions = IntegerField('tour_rev', validators=[InputRequired(), Length(min=1, max=2, message='Must be filled in!')])

    tour_price = FloatField('tour_price', validators=[InputRequired(), NumberRange(min=0, max=None,
                                                                                   message='Price cannot be below $0!')])


class Listing:
    def __init__(
            self,
            tour_name,
            tour_desc,
            tour_price,
            tg_uid,
            tour_loc,
            tour_revs,
            tour_itinerary,
            tour_img=''
    ):

        self.__tour_name = ''
        self.set_tour_name(tour_name)

        self.__tour_desc = ''
        self.set_tour_desc(tour_desc)

        self.__tour_price = 0
        self.set_tour_price(tour_price)

        self.__tour_location = []
        self.set_tour_location(tour_loc)

        self.__tour_revisions = 0
        self.set_tour_revisions(tour_revs)

        self.__tour_itinerary = []
        self.set_tour_itinerary(tour_itinerary)

        self.__tour_img = ''
        self.set_tour_img(tour_img)

        self.set_tg_uid(tg_uid)

        self.__date_created = datetime.now()
        self.__tour_rating = 0
        self.__tour_review = []


    def set_tour_name(self, tour_name):
        try:
            assert len(tour_name) <= 30
        except AssertionError:
            print(f"{tour_name} must be less than {30} characters!")
        else:
            self.__tour_name = tour_name

    def set_tour_desc(self, tour_desc):
        self.__tour_desc = tour_desc


    def set_tour_itinerary(self, tour_itinerary):
        try:
            assert type(tour_itinerary) == list
        except AssertionError:
            print(f"{tour_itinerary} must be of type {list}")
        else:
            self.__tour_review.append(tour_itinerary)

    def add_tour_itinerary(self, itinerary):
        try:
            assert type(itinerary) == str
        except AssertionError:
            print(f"{itinerary} must be of type {str}")
        else:
            self.__tour_itinerary.append(itinerary)

    def set_tour_location(self, tour_location):
        try:
            assert type(tour_location) == list
        except AssertionError:
            print(f"{tour_location} must be of type {list}")
        else:
            self.__tour_location.append(tour_location)

    def set_tour_revisions(self, tour_revisions):
        try:
            tour_revisions = int(tour_revisions)
        except ValueError:
            print(f"{tour_revisions} must be of type {int}")
        else:
            self.__tour_revisions = tour_revisions


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
            "tour_desc": self.__tour_desc,
            "tour_itinerary": self.__tour_itinerary,
            "tour_location": self.__tour_location,
            "tour_revisions": self.__tour_revisions,
            "tour_price": self.__tour_price,
            "tour_img": self.__tour_img,
            "date_created": self.__date_created,
            "tour_rating": self.__tour_rating,
            "tour_review": self.__tour_review,
            "tg_uid": self.__tg_uid,
        }
