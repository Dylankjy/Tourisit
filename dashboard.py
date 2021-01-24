import pymongo

# MongoDB connection string
from bson import ObjectId

import models.DashboardIndex as dindex

client = pymongo.MongoClient(
    'mongodb://tourisitUser:desk-kun_did_nothing_wrong_uwu@ip.system.gov.hiy.sh:27017')['Tourisit']

# Collections
db_dashboard = client['Dashboard']

def get_data_for_tg(uid):
    """
    Get index of specific tour guide
    :param uid: Target user's ID
    :return: Data
    """
    query = {
        'uid': ObjectId(uid)
    }

    result = [i for i in db_dashboard.find(query)]
    
    return result[0]
    
    
def create_index(uid):
    """
    Create a new index for tour guide (used when one doesn't already exist)
    :param uid: Target user's ID
    :return: Status of operation.
    """

    # Get entire database data
    database_data = [i for i in db_dashboard.find({"uid": ObjectId(uid)})]

    # Check whether particular user's data already exists
    if database_data != 0:
        return False

    # Create object, implements DashboardIndex
    index = dindex.DashboardIndexEntry(uid)

    # Return object as a BSON dictionary
    payload = index.return_obj()

    # Database Ops: Insert payload into database
    db_dashboard.insert_one(payload)

    return True
