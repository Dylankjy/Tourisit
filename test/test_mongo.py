from models.model import User, Listing, Booking, Transaction, Support, Booking, Chat, Review
from PIL import Image
import base64
import pymongo
from io import BytesIO
buffered = BytesIO()

client = pymongo.MongoClient('mongodb+srv://admin:slapbass@cluster0.a6um0.mongodb.net/test')['Tourisit']


def img_to_base64(img):
    img = Image.open(img).resize((150, 150))
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    return img_str


# USERS
x = User('Jake', 'getbass', 'ejrkrej2JKEKRJEKJR.@JREIJROM')
y = x.return_obj()
print(y)
db = client['Users']
db.insert_one(y)

# LISTINGS
# img_str = img_to_base64('public/imgs/bookings.jpg')
# x = Listings('Gay bars', 'THis is not me', '60', 'iire3', tour_img=img_str)
# y = x.return_obj()
# print(y)
# db = client['Listings']
# db.insert_one(y)
