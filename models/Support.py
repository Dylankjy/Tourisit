from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField
from wtforms.validators import InputRequired, Length

class SupportForm(FlaskForm):
    support_type = SelectField(
        "support_type",
        choices=[('General Enquiry', 'General Enquiry'), ('Report Tour Guide', 'Report Tour Guide'), ('Apply for Verified', 'Apply for Verified'), ('Others', 'Others')],
        validators=[
            InputRequired()
        ]
    )
    content = TextAreaField(
        "content",
        validators=[
            InputRequired(),
            Length(min=0, max=150, message="Bio can only be 150 characters long!")
        ]
    )

class Support:
    def __init__(self,
                 uid,
                 support_type,
                 content,
                 status='Open'
                 ):
        self.__uid = ''
        self.set_uid(uid)

        self.__support_type = ''
        self.set_support_type(support_type)

        self.__content = ''
        self.set_content(content)

        self.__status = 'Open'
        self.set_status(status)

    def set_uid(self, uid):
        self.__uid = uid

    def set_support_type(self, support_type):
        self.__support_type = support_type

    def set_content(self, content):
        self.__content = content

    def set_status(self, status):
        self.__status = status

    def return_obj(self):
        return {
            "uid": self.__uid,
            "support_type": self.__support_type,
            "content": self.__content,
            "status": self.__status,
        }
