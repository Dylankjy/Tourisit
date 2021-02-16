from datetime import datetime, timedelta, date

from flask_wtf import FlaskForm
from wtforms import DateField, TimeField, BooleanField, SubmitField, TextAreaField, RadioField, StringField, \
    DecimalField
from wtforms.validators import InputRequired, Length


# Customer-side
# Book now - default form
class BookingForm(FlaskForm):
    book_date = DateField('book_date', validators=[InputRequired()])
    book_timeslot = RadioField('book_timeslot', validators=[InputRequired()])
    accept_tnc = BooleanField('Accept?', validators=[InputRequired()])

    def date_valid(self, bookdate, tg_booking_list):
        # If there is date input in the booknow form
        if bookdate:
            formatted_date = datetime.strptime(bookdate, "%m/%d/%Y").date()
            tmr_date = date.today() + timedelta(days=1)
            # If the chosen date is tomorrow onwards
            if formatted_date >= tmr_date:
                for booking in tg_booking_list:
                    if booking['book_date']:
                        format_existing_bookdate = datetime.strptime(booking['book_date'], "%m/%d/%Y").date()
                        # If TG already has a booking on the chosen date
                        if format_existing_bookdate == formatted_date:
                            print("Tour on that day")
                            # Check time, if tours overlap, return false
                return True
            elif formatted_date < tmr_date:
                return False
        else:
            return False

    def time_valid(self, booktime):
        if booktime == 'None':
            return False
        else:
            return True


# Payment Gateway Button
class CheckoutForm(FlaskForm):
    submit = SubmitField('Pay & Proceed')


# Request Revisions form
class RevisionForm(FlaskForm):
    revision_text = TextAreaField("revision_text", validators=[InputRequired(), Length(min=0, max=75, message="")])
    submit = SubmitField("Request a Revision", validators=[InputRequired()])


# Submit Requirements form
class RequirementsForm(FlaskForm):
    req_text = TextAreaField("revision_text", validators=[InputRequired(), Length(min=0, max=75, message="")])
    submit = SubmitField("Submit your Requirements", validators=[InputRequired()])


# TG-side
# Edit Plan form
class EditPlan(FlaskForm):
    tour_items = StringField('tour_items')
    tour_date = DateField('tour_date', validators=[InputRequired()])
    tour_starttime = TimeField('tour_starttime', validators=[InputRequired()])
    tour_endtime = TimeField('tour_endtime', validators=[InputRequired()])
    tour_price = DecimalField('tour_price')


# Additional Info form field
class AddInfoForm(FlaskForm):
    AddInfo = TextAreaField("AddInfo", validators=[Length(min=0, max=75, message="")])


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
            chat_id,
            revisions,
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
        self.__revisions = revisions
        self.__process_step = process_step
        self.__book_charges = {
            'baseprice': float(book_baseprice),
            'customfee': float(book_customfee),
            'revisionfee': float(0)}
        self.__book_info = ""
        self.__book_chat = chat_id
        self.__completed = 0
        self.__customer_req = {'requirements': '', 'revision': ''}

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
            "revisions": self.__revisions,
            "process_step": self.__process_step,
            "book_charges": self.__book_charges,
            "book_info": self.__book_info,
            "book_chat": self.__book_chat,
            "customer_req": self.__customer_req
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
