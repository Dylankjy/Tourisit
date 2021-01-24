from io import BytesIO

from models.Format import ObjectId

import pymongo

buffered = BytesIO()

client = pymongo.MongoClient('mongodb://tourisitUser:desk-kun_did_nothing_wrong_uwu@ip.system.gov.hiy.sh:27017')['Tourisit']

# tour_name = 'Best of Kampong Glam'
# tour_brief= 'Walk around this architectural marvel that™s both a cultural attraction and a historical museum'
# tour_desc = 'Swing by Kampong Gelam, Singapore™s oldest quarter, to get to know the culture and traditions of the Malay community and Islam. Discover the origins of the old Royal Palace and Sultan Mosque. You"ll also be taught how to tie a sarong (a large length of fabric often wrapped around the waist and worn by men and women throughout most of Indonesia). Don™t miss Haji Lane, one of Singapore™s most popular streets known for its cool backdrops and quirky shops.'
# tour_price = 70
# tg_uid = '5fde1b5bdf4fe3bc527058f1'
# tour_img = 'hi'

db = client['Chats']

# x = list(db.find({"$sample": {"size":1}}))

# query = [{"$match": {"participants": 1}},
#          {"$sample": {"size": 1}}]

user = ObjectId('600666f7ccab3b102fce39fb')
tg = ObjectId('5feafbbf4dbad8d4b8614958')


query = {'participants': {"$in": [tg, user]}, 'chat_type': 'UwU'}
x = list(db.find(query))

print(x[0]['_id'])

# query = {}
# x = list(db.find(query))
#
# updated = {
#     "$set": {
#         'tour_visibility': 1,
#     }}
#
# db.update_many(query, updated)


# x = list(db.find())[:12]
# y = len(x)
# print(y)

# result_listings = list(db.find())
# for listing in result_listings:
#     listing['_id'] = JSONEncoder().encode(listing['_id'])
#     listing['date_created'] = str(listing['date_created'])
#     listing['tour_img'] = str(listing['tour_img'])
# print(result_id)

# for listing in result_listings:
#
#     listing = [value.encode('utf-8') for value in listing]

# y = json.dumps({"results": result_listings})

# all_listings = list(i['tour_name'] for i in db.find())
# print(all_listings)
#
# text = 'i'
# result = [c for c in all_listings if str(text).lower() in c.lower()]
# x = list(i for i in db.find({'tour_name': {'$in': result}}))
# print(x[1])

# co = True
# while co:
#     text = input('txt:')
#     # all_listings = list(i['tour_name'] for i in db.find())
#     # print(all_listings)
#     result = [c for c in all_listings if str(text).lower() in c.lower()]
#     x = list(i['tour_name'] for i in db.find({'tour_name': {'$in': result }}))
#     print(x)
#     cont = input('co:?')
#     if cont == 'n':
#         co = False


# x = list(db.find())
# for i in x:
#     print(i['_id'])
#
#
# def img_to_base64(img):
#     img = Image.open(img).resize((150, 150))
#     img.save(buffered, format="JPEG")
#     img_str = base64.b64encode(buffered.getvalue())
#     return img_str


# co = True
# while co:
#     tour_name = input('Name:')
#     tour_brief = input('Tour brief:')
#     tour_desc = input('Tour Desc')
#     tour_price = input('Tour price')
#     tg_uid = '5fde1b5bdf4fe3bc527058f1'
#     tour_img = img_to_base64('../public/imgs/bookings.jpg')
#     x = Listing(tour_name, tour_brief, tour_desc, tour_price, tg_uid, tour_img)
#     y = x.return_obj()
#     db = client['Listings']
#     db.insert_one(y)
#     cont = input('cont?:')
#     if cont == 'f':
#         co = False


# db = client['Listings']
# x = list(db.find())
# print(x[0]['tour_brief'])
# # USERS
# x = User('Jake', 'getbass', 'ejrkrej2JKEKRJEKJR.@JREIJROM')
# y = x.return_obj()
# print(y)
# db = client['Users']
# db.insert_one(y)

# LISTINGS
# img_str = img_to_base64('public/imgs/bookings.jpg')
# x = Listings('bars', 'THis is not me', '60', 'iire3', tour_img=img_str)
# y = x.return_obj()
# print(y)
# db = client['Listings']
# db.insert_one(y)
