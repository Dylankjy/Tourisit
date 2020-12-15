from model import User, Listing, Bookings, Transactions, Support

import pymongo

db = pymongo.MongoClient('mongodb+srv://admin:slapbass@cluster0.a6um0.mongodb.net/test')
Listings = db['Tourisit']['Listings']

