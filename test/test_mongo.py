from datetime import datetime
from io import BytesIO
from statistics import mean

import pymongo

from models.Format import ObjectId

buffered = BytesIO()

client = pymongo.MongoClient('mongodb://tourisitUser:desk-kun_did_nothing_wrong_uwu@ip.system.gov.hiy.sh:27017')[
    'Tourisit']

# tour_name = 'Best of Kampong Glam'
# tour_brief= 'Walk around this architectural marvel that™s both a cultural attraction and a historical museum'
# tour_desc = 'Swing by Kampong Gelam, Singapore™s oldest quarter, to get to know the culture and traditions of the Malay community and Islam. Discover the origins of the old Royal Palace and Sultan Mosque. You"ll also be taught how to tie a sarong (a large length of fabric often wrapped around the waist and worn by men and women throughout most of Indonesia). Don™t miss Haji Lane, one of Singapore™s most popular streets known for its cool backdrops and quirky shops.'
# tour_price = 70
# tg_uid = '5fde1b5bdf4fe3bc527058f1'
# tour_img = 'hi'


db = client['Listings']
db_transactions = client['Transactions']


# ini_list.sort(key = lambda x: datetime.strptime(x['d.o.b'], '%Y-%m-%d'))

# Average Earning per tour
# Positive
# Negative

def get_pos_neg(uid):
    x = list(db.find({"tg_uid": ObjectId(uid), "tour_reviews": {"$ne": "null"}}, {"_id": 0, "tour_reviews": 1}))
    x = [x[i] for i in range(len(x)) if len(x[i]['tour_reviews']) != 0]
    stars = []
    d = {}
    for listing in x:
        for review in listing['tour_reviews']:
            if int(review['stars']) > 2:
                stars.append('p')
            else:
                stars.append('n')

    d['Positive'] = stars.count('p')
    d['Negative'] = stars.count('n')

    return d


# print(get_pos_neg('600666f7ccab3b102fce39fb'))


def get_earning_breakdown(uid):
    query = [
        {"$match": {"tg_uid": ObjectId(uid)}},
        {"$group": {"_id": {"month": "$month_paid", "year": "$year_paid"}, "total": {"$sum": "$earnings"}}},
        {"$sort": {"year": -1}}

        # {"$group": {"_id": {"$and": ["$month_paid"]}, "total": {"$sum": "$earnings"}}},
    ]

    transactions = list(db_transactions.aggregate(query))
    for i in transactions:
        i['Date'] = f"{i['_id']['month']}-{i['_id']['year']}"
        i["Month"] = i['_id']['month']
        i["Year"] = i['_id']['year']
        del i['_id']

    # transactions.sort(key=lambda x:x['Date'])
    transactions.sort(key=lambda x: datetime.strptime(x['Date'], '%m-%Y'))
    return transactions


# xgg = get_earning_breakdown('600666f7ccab3b102fce39fb')
# print(xgg)

def er(uid):
    query = [
        {"$match": {"tg_uid": ObjectId(uid)}},
        {"$group": {"_id": {"month": "$month_paid", "year": "$year_paid"}, "total_cost": {"$sum": "$earnings"},
                    "total_tours": {'$sum': 1}}},
        {"$sort": {"year": -1}}

        # {"$group": {"_id": {"$and": ["$month_paid"]}, "total": {"$sum": "$earnings"}}},
    ]

    transactions = list(db_transactions.aggregate(query))

    total_cost = []
    total_tours = []
    for i in transactions:
        total_cost.append(i['total_cost'])
        total_tours.append(i['total_tours'])

    total_cost = sum(total_cost)
    total_tours = sum(total_tours)
    avg = total_cost / total_tours
    return round(avg, 2)


# x = er('600666f7ccab3b102fce39fb')
#
# print(x)


def get_satisfaction_rate(uid):
    x = list(db.find({"tg_uid": ObjectId(uid), "tour_reviews": {"$ne": "null"}}, {"_id": 0, "tour_reviews": 1}))
    x = [x[i] for i in range(len(x)) if len(x[i]['tour_reviews']) != 0]
    l = []
    for listing in x:
        # print(listing)
        d = {}
        for review in listing['tour_reviews']:
            print(review)
            booking_id = review['booking']
            # print(booking_id)
            book = list(db_transactions.find({'booking': ObjectId(booking_id)}))[0]
            date = f"{book['month_paid']}-{book['year_paid']}"
            if 'date' in d:
                d['stars'].append(int(review['stars']))
            else:
                d['date'] = date
                d['stars'] = [int(review['stars'])]

        d['stars'] = mean(d['stars'])
        l.append(d)

    l.sort(key=lambda x: datetime.strptime(x['date'], '%m-%Y'))

    return l

# x = get_satisfaction_rate('600666f7ccab3b102fce39fb')
# print(x)
# print(x)

# for idx,listings in enumerate(x):
# if len(listings['tour_reviews']) == 0:
#     x.pop()


# print(x)
# x = [x[i] if len(x[i]['tour_reviews']) != 0 for i in range(len(x))]

# l = []
# this is the dictionary containing the mean starts

# l = []
# for listing in x:
#     # print(listing)
#     d = {}
#     for review in listing['tour_reviews']:
#         print(review)
#         booking_id = review['booking']
#         # print(booking_id)
#         book = list(db_transactions.find({'booking': ObjectId(booking_id)}))[0]
#         date = f"{book['month_paid']}-{book['year_paid']}"
#         if 'date' in d:
#             d['stars'].append(int(review['stars']))
#         else:
#             d['date'] = date
#             d['stars'] = [int(review['stars'])]
#
#     d['stars'] = mean(d['stars'])
#     l.append(d)
# if len(date) == 0:
#     d['date'] = date
#     d['stars'] = [int(review['stars'])]
# if date in d['date']:
#     d['date'].append(int(review['stars']))
# else:
#     d['date'] = date
#     d['stars'] = [int(review['stars'])]

# d['date'] = mean(d['date'])
# l.append(d)

#     print(d)
#
# l.sort(key=lambda x: datetime.strptime(x['date'], '%m-%Y'))
# print(l)
#
# rr = [{'date': 1-20, 'stars': 4.5}, {'date': 1-60, 'stars': 2}]

# print(l)

# l.sort(key=lambda x: datetime.strptime(x['Date'], '%m-%Y'))
# print(l)

# y = [{'tour_reviews': [{'stars': '4', 'text': 'Good tour', 'reviewer': ObjectId('601268c9fc45385ec00f554c'), 'reviewee': ObjectId('600666f7ccab3b102fce39fb'), 'booking': ObjectId('60126b4a996215452fb3d430'), 'listing': ObjectId('601256e4758ced26954f4d7f')}, {'stars': 5, 'text': 'Great guy', 'reviewer': ObjectId('601252cf758ced26954f4d77'), 'reviewee': ObjectId('600666f7ccab3b102fce39fb'), 'booking': ObjectId('6017bc6cbbf2d69d3990c292'), 'listing': ObjectId('601256e4758ced26954f4d7f')}]}]

#  9
# print(x)
# y = [{'tour_reviews': [{'stars': '4', 'text': 'Good tour', 'reviewer': ObjectId('601268c9fc45385ec00f554c'), 'reviewee': ObjectId('600666f7ccab3b102fce39fb'), 'booking': ObjectId('60126b4a996215452fb3d430'), 'listing': ObjectId('601256e4758ced26954f4d7f')}, {'stars': 5, 'text': 'Great guy', 'reviewer': ObjectId('601252cf758ced26954f4d77'), 'reviewee': ObjectId('600666f7ccab3b102fce39fb'), 'booking': ObjectId('6017bc6cbbf2d69d3990c292'), 'listing': ObjectId('601256e4758ced26954f4d7f')}]}]


# for i in range(len(test_list)):
#     if test_list[i]['id'] == 2:
#         del test_list[i]
#         break


# items = list(db.find({'tg_uid': ObjectId('600666f7ccab3b102fce39fb')}))[:3]
# print(items)
# db_booking = client['Bookings']
#
# book_id = '600d72de9a9cad41198a0017'

# item = list(db.find({'_id': ObjectId(book_id)}))
# # x = item[0]['tour_reviews']
# # print(len(x))
# tmp1 = list(map(lambda i: i['tour_reviews'], item))[0]
# print(len(tmp1))


# y = list(map(lambda x: x['book_time'], x))
# z = list(set(y))
# print(z)
# print(x)
# dates = list(map(lambda x: x['book_date'], x))
# times = list(map(lambda x: x['book_time'], x))
# print(dates)
# print(times)
# z = tuple(zip(dates, times))
# print(z)
# print(dict(z))

# q = dict.fromkeys(dates)
# q = {}
#
# for date, time in z:
#     if date in q:
#         q[date].append(time)
#     else:
#         q[date] = [time]
#
# print(q)

# (('01/14/2021', ['10:00 AM - 1:00 PM']), ('01/14/2021', ['4:00 PM - 7:00 PM']), ('01/08/2021', ['6:00 AM - 9:00 AM'])) TO {'01/14/2021': ['4:00 PM - 7:00 PM', '10:00 AM - 1:00 PM'], '01/08/2021': ['6:00 AM - 9:00 AM']}

# dayTonumber = {'Mon': 1, 'Tues':2, 'Wed': 3, 'Thurs': 4, 'Fri': 5, 'Sat': 6, 'Sun': 0}
# x = list(db.find({'_id': ObjectId('600cc14fa87f5823e1c7c1fe')}))[0]['tour_days']
# y = list(map(lambda i: dayTonumber[i], x))
# z = [*range(7)]
# print(z)
# print(y)
# print(list(set(z) - set(y)))

# x = list(db_booking.find({'listing_id': ObjectId('600cc14fa87f5823e1c7c1fe'), 'completed': 0}))

# data = {'stars': None, 'text': 'tset', 'reviewer': ObjectId('600666f7ccab3b102fce39fb'), 'reviewee': ObjectId('5feafbbf4dbad8d4b8614958'), 'booking': ObjectId('600d31af52d1ea317620975c'), 'listing': ObjectId('600cc14fa87f5823e1c7c1fe')}
# updated = {'$push': {'tour_reviews': data}}

# query = {'_id': ObjectId('600bdb4dd0fe9f3882f9c06d')}

# db.update_one(query, updated)
# book_id = ObjectId('600d31af52d1ea317620975c')
# query = {'tour_reviews': {"$in": {"booking": book_id}}, '_id': db_booking['listing_id']}
# x = list(db.find(query))
# print(x)
# y = list(map(lambda i:i['tour_reviews'], x))[0]
# z = list(map(lambda i:i['booking'], y))
# print(z)


# x = list(db.find({"$sample": {"size":1}}))

# query = [{"$match": {"participants": 1}},
#          {"$sample": {"size": 1}}]


# chat_db = client['Chats']

# user = ObjectId('600666f7ccab3b102fce39fb')
# tg = ObjectId('5feafbbf4dbad8d4b8614958')
#
#
# query = {'participants': {"$in": [tg, user]}, 'chat_type': 'UwU'}
# x = list(chat_db.find(query))
#
# print(x[0]['_id'])

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
