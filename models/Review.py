from flask_wtf import FlaskForm
from wtforms import TextAreaField, RadioField
from wtforms.validators import InputRequired


class ReviewForm(FlaskForm):
    rating = RadioField('label', choices=[(1,'*'),(2,'**'),(3,'***'),(4,'****'),(5,'******')])
    review_text = TextAreaField('review_text', validators=[InputRequired()])


class Review:
    def __init__(self, stars, text, reviewer_id, reviewee_id, booking, listing):
        self.__stars = stars
        self.__text = text
        self.__reviewer_id = reviewer_id
        self.__reviewee_id = reviewee_id
        self.__booking = booking
        self.__listing = listing

    def return_obj(self):
        return {
            "stars": self.__stars,
            "text": self.__text,
            "reviewer": self.__reviewer_id,
            "reviewee": self.__reviewee_id,
            "booking": self.__booking,
            "listing": self.__listing
        }
