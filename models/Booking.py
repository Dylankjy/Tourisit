from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import DateField, TimeField, BooleanField, SubmitField
from wtforms.validators import InputRequired

# Book now - default form
class BookingForm(FlaskForm):
    book_date = DateField('book_date', validators=[InputRequired()])
    book_time = TimeField('book_time', validators=[InputRequired()])
    accept_tnc = BooleanField('Accept?', validators=[InputRequired()])
    book_submit = SubmitField('Book Now')

# oh no.
# Book now - Customise tour
class CustomForm(FlaskForm):
    submit = SubmitField('Customise Tour', validators=[InputRequired()])

# Book now - Chat with TG
class ChatForm(FlaskForm):
    submit = SubmitField(validators=[InputRequired()])

# Payment Gateway Button
class CheckoutForm(FlaskForm):
    submit = SubmitField('Pay & Proceed')


# add charges
class Booking:
    def __init__(
            self,
            tg_uid,
            cust_uid,
            listing_id,
            book_date,
            book_time,
            book_baseprice,
            book_customfee,
            book_duration,
            timeline_content,
            process_step,
    ):
        self.__tg_uid = tg_uid
        self.__cust_uid = cust_uid
        self.__listing_id = listing_id
        self.__book_date = book_date
        self.__book_time = book_time
        # self.__book_datetime = ''
        # self.set_book_datetime(book_date, book_time)
        self.__book_duration = book_duration
        self.__timeline_content = timeline_content
        self.__process_step = process_step
        self.__book_charges = {
            'baseprice': float(book_baseprice),
            'customfee': float(book_customfee)}
        self.__book_info = ""
        self.__book_chat = ''
        self.__completed = 0

    def set_book_datetime(self, book_date, book_time):
        try:
            book_datetime = book_date + " " + book_time
            book_datetime = datetime.strptime(book_datetime, '%Y-%m-%d %H:%M')
            book_datetime = book_datetime.isoformat()
        except BaseException:
            print("An Error occured.")
        else:
            self.__book_datetime = book_datetime

    def set_book_duration(self, book_duration):
        self.__book_duration = book_duration

    def set_book_info(self, book_info):
        self.__book_info = book_info

    def step_forward(self):
        self.__process_step += 1

    def return_obj(self):
        return {
            "tg_uid": self.__tg_uid,
            "cust_uid": self.__cust_uid,
            "listing_id": self.__listing_id,
            "book_date": self.__book_date,
            "book_time": self.__book_time,
            # "book_datetime": self.__book_datetime,
            "book_duration": self.__book_duration,
            "timeline_content": self.__timeline_content,
            "process_step": self.__process_step,
            "book_charges": self.__book_charges,
            "book_info": self.__book_info,
            "book_chat": self.__book_chat,
            "completed": self.__completed
        }


def calculate_totalcost(book_charges):
    try:
        totalcost = float(book_charges['baseprice'])
        for i in book_charges['additions']:
            totalcost += i
        for i in book_charges['reductions']:
            totalcost -= i
        if totalcost > 0:
            return round(totalcost, 2)
    except BaseException:
        print("An error occured while trying to compute the total cost. Check Datatypes or negative inputs.")
