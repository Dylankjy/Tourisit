from datetime import datetime
import os

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, FloatField, IntegerField, SelectField, SelectMultipleField, widgets, SubmitField
from wtforms.validators import InputRequired, Length, NumberRange, ValidationError


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class CustomSelectField(FlaskForm):
    '''
        start_name (PARAMS): The start of the id. This is constant for all generated ids
        options (PARAMS): A list of all the options. This is appended behind the start_name
    '''

    def __init__(self, fieldName, start_name, options):
        self.__fieldName = fieldName
        self.__start_name = start_name
        self.__options = options

    def return_Field(self):
        kws = {'id': f'{self.__start_name}-{self.__options}'}
        return SelectField(
            self.__fieldName, choices=self.__options, render_kw=kws)


# def time_check(form, field, start_field):
#     if time_list.index(field.data) < time_list.index(start_field.data):
#         raise ValidationError('End time wrong!')


time_list = ['6:00 AM', '6:30 AM', '7:00 AM', '7.30 AM', '8:00 AM', '8:30 AM', '9:00 AM',
              '9:30 AM', '10:00 AM', '10:30 AM', '11:00 AM', '11:30 AM', '12:00 PM',
              '12:30 PM', '1:00 PM', '1:30 PM', '2:00 PM', '2:30 PM', '3:00 PM', '3:30 PM',
              '4:00 PM', '4:30 PM', '5:00 PM', '5:30 PM', '6:00 PM', '6:30 PM', '7:00 PM',
              '7:30 PM', '8:00 PM', '8:30 PM', '9:00 PM', '9:30 PM', '10:00 PM', '10:30 PM', '11:00 PM']


# Add no. of revisions, itineary, location
class ListingForm(FlaskForm):

    tour_name = StringField('tour_name', validators=[InputRequired(), Length(min=1, max=30,
                                                                             message='Name can only be 30 characters long!')])

    tour_desc = TextAreaField('tour_desc', validators=[InputRequired()])

    tour_start_time = SelectField('tour_start_time', choices=time_list, validators=[InputRequired()])

    tour_end_time = SelectField('tour_end_time', choices=time_list, validators=[InputRequired()])

    tour_days = MultiCheckboxField('tour_days', choices=[('Mon', 'Monday'), ('Tues','Tuesday'),('Wed', 'Wednesday'), ('Thurs','Thursday'), ('Fri', 'Friday'), ('Sat','Saturday'), ('Sun','Sunday')], validators=[InputRequired('Please select at least one available day')])

    # Tour itinerary
    tour_items = StringField('tour_items')

    # tour_items_list = FieldList(HiddenField('tour_items_list', validators=[InputRequired()]))
    tour_size = IntegerField('tour_size', validators=[InputRequired(), NumberRange(min=0, max=8, message="Max Participants must be at least 1 and cannot exceed 8")])

    tour_loc = SelectField('tour_loc', choices=['Ang Mo Kio', 'Bedok', 'Bishan', 'Bukit Batok', 'Bukit Merah',
                                          'Bukit Panjang', 'Bukit Timah', 'Chinatown', 'Choa Chu Kang', 'Clementi', 'Changi',
                                          'Geylang', 'Hougang', 'Jurong East', 'Jurong West', 'Kallang',
                                          'Marine Parade', 'Orchard', 'Pasir Ris', 'Punggol', 'Queenstown',
                                          'Sembawang', 'Sengkang', 'Serangoon', 'Sentosa', 'Tampines', 'Toa Payoh',
                                          'Woodlands', 'Yishun'] )

    # tour_loc = CustomSelectField(fieldName='tour_loc', start_name='loc',
    #                              options=['Ang Mo Kio', 'Bedok', 'Bishan', 'Bukit Batok', 'Bukit Merah',
    #                                       'Bukit Panjang', 'Bukit Timah',
    #                                       'Choa Chu Kang', 'Clementi', 'Changi', 'Geylang', 'Hougang', 'Jurong East',
    #                                       'Jurong West',
    #                                       'Kallang', 'Marine Parade', 'Orchard', 'Pasir Ris', 'Punggol', 'Queenstown',
    #                                       'Sembawang', 'Sengkang',
    #                                       'Serangoon', 'Sentosa', 'Tampines', 'Toa Payoh', 'Woodlands',
    #                                       'Yishun']).return_Field()

    tour_img = FileField('tour_img', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Only .jpg, .jpeg and .png images are allowed!')])

    tour_revisions = IntegerField('tour_rev', validators=[InputRequired(),
                                                          NumberRange(min=0, message='Need a minimum of 1 revision!')])

    tour_price = FloatField('tour_price', validators=[InputRequired(), NumberRange(min=0, max=None,
                                                                                   message='Price cannot be below $0!')])

    # tour_submit = SubmitField('tour_submit', validators=[InputRequired()])

    # def validate(self, tour_end_time):
    #     rv = FlaskForm.validate(self)
    #     if not rv:
    #         return False
    #
    #     print(self.tour_end_time.data)
    #     if time_list.index(self.tour_end_time.data) < time_list.index(self.tour_end_time.data):
    #         self.tour_end_time.errors.append('End time must be later than start time!')
    #         return False
    #
    #     return True

    def check_time(self):
        end_idx = time_list.index(self.tour_end_time.data)
        start_idx = time_list.index(self.tour_start_time.data)
        if end_idx < start_idx:
            # Must convert to a list first (So can append) and then convert back to the tuple (original form)
            tmp = list(self.tour_end_time.errors)
            tmp.append('End time must be later than start time!')
            self.tour_end_time.errors = tuple(tmp)
            return False
        return True


    # def check_filesize(self, filesize):
    #     if int(filesize) <= 1 * 1024 * 1024:
    #         return True
    #     else:
    #         return False


    def validate(self):
        #This is the default flask validation rules (Which you define in the wtforms fields)
        if not FlaskForm.validate(self):
            return False

        # Provided that the original flask validation passes, you now pass it through an additional validation (Check the timings)
        result = self.check_time()
        return result


# print(time_list.index('9:00 AM'))


class Listing:
    def __init__(
            self,
            tour_name,
            tour_desc,
            tour_price,
            tg_uid,
            tour_location,
            tour_revs,
            tour_itinerary,
            tour_days,
            tour_time,
            tour_img='',
            tour_size='',
            tour_bookings={}
    ):

        self.__tour_name = ''
        self.set_tour_name(tour_name)

        self.__tour_desc = ''
        self.set_tour_desc(tour_desc)

        self.__tour_days = ''
        self.set_tour_days(tour_days)

        self.__tour_times = ''
        self.set_tour_time(tour_time)

        self.__tour_price = 0
        self.set_tour_price(tour_price)

        self.__tour_location = ''
        self.set_tour_location(tour_location)

        self.__tour_revisions = 0
        self.set_tour_revisions(tour_revs)

        self.__tour_itinerary = ''
        self.set_tour_itinerary(tour_itinerary)

        self.__tour_img = ''
        self.set_tour_img(tour_img)

        self.__tour_size = ''
        self.set_tour_size(tour_size)

        self.set_tg_uid(tg_uid)

        self.__visibility = 1
        self.__date_created = datetime.now()
        self.__tour_rating = 0
        self.__tour_reviews = []
        self.__tour_bookings = tour_bookings

    def set_tour_name(self, tour_name):
        try:
            assert len(tour_name) <= 30
        except AssertionError:
            print(f"{tour_name} must be less than {30} characters!")
        else:
            self.__tour_name = tour_name

    def set_tour_days(self, tour_days):
        self.__tour_days = tour_days

    def set_tour_time(self, tour_times):
        self.__tour_times = tour_times

    def set_tour_desc(self, tour_desc):
        self.__tour_desc = tour_desc

    def set_tour_itinerary(self, tour_itinerary):
        try:
            assert isinstance(tour_itinerary, list)
        except AssertionError:
            print(f"{tour_itinerary} must be of type {list}")
        else:
            self.__tour_itinerary = tour_itinerary

    def add_tour_itinerary(self, itinerary):
        try:
            assert isinstance(itinerary, str)
        except AssertionError:
            print(f"{itinerary} must be of type {str}")
        else:
            self.__tour_itinerary.append(itinerary)

    def set_tour_location(self, tour_location):
        try:
            assert isinstance(tour_location, list)
        except AssertionError:
            print(f"{tour_location} must be of type {list}")
        else:
            self.__tour_location = tour_location

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

    def set_tour_size(self, tour_size):
        self.__tour_size = tour_size

    def set_tour_img(self, tour_img):
        self.__tour_img = tour_img

    def set_tour_rating(self, tour_rating):
        try:
            tour_rating = float(tour_rating)
        except ValueError:
            print(f"{tour_rating} must be of type {float}")
        else:
            self.__tour_rating = tour_rating

    def set_tour_reviews(self, tour_reviews):
        try:
            assert isinstance(tour_reviews, list)
        except AssertionError:
            print(f"{tour_reviews} must be of type {list}")
        else:
            self.__tour_reviews.append(tour_reviews)

    def set_tg_uid(self, tg_uid):
        self.__tg_uid = tg_uid

    def return_obj(self):
        return {
            "tour_name": self.__tour_name,
            "tour_desc": self.__tour_desc,
            "tour_days": self.__tour_days,
            "tour_time": self.__tour_times,
            "tour_itinerary": self.__tour_itinerary,
            "tour_location": self.__tour_location,
            "tour_revisions": self.__tour_revisions,
            "tour_price": self.__tour_price,
            "tour_img": self.__tour_img,
            "date_created": self.__date_created,
            "tour_rating": self.__tour_rating,
            "tour_reviews": self.__tour_reviews,
            "tour_size": self.__tour_size,
            "tg_uid": self.__tg_uid,
            "tour_visibility": self.__visibility,
            "tour_bookings": self.__tour_bookings
        }

