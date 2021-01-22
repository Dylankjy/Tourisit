import pymongo

# MongoDB connection string
from bson import ObjectId

client = pymongo.MongoClient(
    'mongodb://tourisitUser:desk-kun_did_nothing_wrong_uwu@ip.system.gov.hiy.sh:27017')['Tourisit']

# Collections
db_dashboard = client['Dashboard']

def get_data_for_tg(uid):
    query = {
        uid: ObjectId(uid)
    }

    result = [i for i in db_dashboard.find(query)]