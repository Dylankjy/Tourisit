from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, StringField
from wtforms.validators import InputRequired, Length, Optional


class SupportForm(FlaskForm):
    support_type = SelectField(
        "support_type",
        choices=[('General Enquiry', 'General Enquiry'), ('Report User', 'Report User'), ('Report Tour Guide', 'Report Tour Guide'),
                 ('Apply for Verified', 'Apply for Verified'), ('Others', 'Others')],
        validators=[
            InputRequired()
        ]
    )
    link = StringField(
        "link",
        validators=[
            Optional(),
            Length(
                min=0,
                max=300,
                message="Tour Guide profile link can only be 300 characters long!")
        ]
    )
    content = TextAreaField(
        "content",
        validators=[
            InputRequired(),
            Length(
                min=0,
                max=500,
                message="Message can only be 500 characters long!")
        ]
    )

class StatusForm(FlaskForm):
    status =
class Support:
    def __init__(self,
                 uid,
                 support_type,
                 content,
                 link,
                 status='Open'
                 ):
        self.__uid = ''
        self.set_uid(uid)

        self.__support_type = ''
        self.set_support_type(support_type)

        self.__content = ''
        self.set_content(content)

        self.__link = ''
        self.set_tg_link(link)

        self.__status = 'Open'
        self.set_status(status)

    def set_uid(self, uid):
        self.__uid = uid

    def set_support_type(self, support_type):
        self.__support_type = support_type

    def set_content(self, content):
        self.__content = content

    def set_tg_link(self, link):
        self.__link = link

    def set_status(self, status):
        self.__status = status

    def return_obj(self):
        return {
            "uid": self.__uid,
            "support_type": self.__support_type,
            "link": self.__link,
            "content": self.__content,
            "status": self.__status
        }
