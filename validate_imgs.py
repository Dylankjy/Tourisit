import base64
import imghdr
from io import BytesIO

buffered = BytesIO()


def img_to_base64(img):
    image_string = str(base64.b64encode(img.read()))
    img_string_edited = image_string.strip("b'")
    img_string_edited = img_string_edited.strip("'")
    return img_string_edited


def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return "yes"
    return 'No'
