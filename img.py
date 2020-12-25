import base64
from io import BytesIO

from PIL import Image

buffered = BytesIO()


def img_to_base64(img):
    img = Image.open(img).resize((150, 150))
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    return img_str


img_str = img_to_base64('public/imgs/bookings.jpg')
print(img_str)
