from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms.validators import InputRequired


class ReviewForm(FlaskForm):
    review_text = TextAreaField('review_text', validators=[InputRequired()])


class Review:
    def __init__(self, stars, text, reviewer_id, reviewee_id):
        self.__stars = stars
        self.__text = text
        self.__reviewer_id = reviewer_id
        self.__reviewee_id = reviewee_id

    def return_obj(self):
        return {
            "stars": self.__stars,
            "text": self.__text,
            "reviewer": self.__reviewer_id,
            "reviewee": self.__reviewee_id,
        }
