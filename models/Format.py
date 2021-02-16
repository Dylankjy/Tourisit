import base64
import json
from io import BytesIO

from PIL import Image
from bson import ObjectId

buffered = BytesIO()


# This encodes a Mongodb Element into a JSON format accepted by Flask
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


# FOR FLASK FORMS

# This converts the image from request.forms to a base64 string
def img_to_base64(img):
    image_string = str(base64.b64encode(img.read()))
    img_string_edited = image_string.strip("b'")
    img_string_edited = img_string_edited.strip("'")
    return img_string_edited


# This converts a png/jpeg image into a base64 string
def file_to_base64(img, size=(150, 150)):
    img = Image.open(img).resize(size)
    img.save(buffered, format="JPEG")
    img_str = str(base64.b64encode(buffered.getvalue()))
    img_str = img_str.strip("b'")
    img_str = img_str.strip("'")
    return img_str


# This converts the request.form.getlist to an actual python list
def formToArray(formListField):
    formListField = formListField[0].replace("None,", '')
    formListField = formListField.replace(",None", '')
    formListField = formListField.split('#$%^#,')
    # Remove the special seperators for the last list element
    formListField[-1] = formListField[-1].strip('#$%^#')
    # Make sure there is no empty strings
    tour_itinerary = [i for i in formListField if i.strip() != '']
    return tour_itinerary


# Takes an array and sorts it (From Mon - Sun sequentially)
def sortDays(dayArr):
    intToDate = {0: 'Mon', 1: 'Tues', 2: 'Wed', 3: 'Thurs', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
    dateToInt = {'Mon': 0, 'Tues': 1, 'Wed': 2, 'Thurs': 3, 'Fri': 4, 'Sat': 5, 'Sun': 6}

    y = sorted(list(map(lambda y: dateToInt[y], dayArr)))
    z = list(map(lambda x: intToDate[x], y))
    return z
