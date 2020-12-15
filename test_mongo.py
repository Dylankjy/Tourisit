from model import *

import pymongo

db = pymongo.MongoClient('mongodb+srv://admin:slapbass@cluster0.a6um0.mongodb.net/test')
Listings = db['Tourisit']['Listings']