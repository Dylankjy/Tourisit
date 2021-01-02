from flask_wtf import FlaskForm
from wtforms import DateField, TimeField, BooleanField
from wtforms.validators import InputRequired, DataRequired
from datetime import datetime

class BookingForm(FlaskForm):
    book_date = DateField('book_date', validators=[InputRequired()])
    book_time = TimeField('book_time', validators=[InputRequired()])
    accept_tnc = BooleanField('Accept?', validators=[InputRequired()])


class Booking:
    def __init__(
            self,
            tg_uid,
            cust_uid,
            listing_id,
            book_date,
            book_time,
            book_duration,
            timeline_content,
            process_step,
    ):
        self.__tg_uid = tg_uid
        self.__cust_uid = cust_uid
        self.__listing_id = listing_id
        self.__book_chat = []
        self.set_book_datetime(book_date, book_time)
        self.__book_duration = book_duration
        self.__book_info = ""
        self.__timeline_content = timeline_content
        self.__process_step = process_step

    def set_book_datetime(self, book_date, book_time):
        try:
            book_datetime = datetime.combine(book_date, book_time)
            datetime.book_datetime.isoformat()
        except:
            print("An Error occured.")
        else:
            self.__book_datetime = book_datetime

    def set_book_duration(self, book_duration):
        self.__book_duration = book_duration

    def set_book_info(self, book_info):
        self.__book_info = book_info

    def step_forward(self):
        self.__process_step += 1

    def payment_made(self):
        self.__process_step = 6

    def return_obj(self):
        return {
            "tg_uid": self.__tg_uid,
            "cust_uid": self.__cust_uid,
            "listing_id": self.__listing_id,
            "book_chat": self.__book_chat,
            "book_datetime": self.__book_datetime,
            "book_duration": self.__book_duration,
            "book_info": self.__book_info,
            "timeline_content": self.__timeline_content,
            "process_step": self.__process_step,
        }
