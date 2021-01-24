import pymongo
import xlsxwriter

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

def update_index(uid, new_data):
    """
    Update earnings
    :param uid: Target user's ID
    :param new_data: Earnings data (in integer type)
    :return: Updated data
    """
    query = {
        'uid': ObjectId(uid)
    }

    result = [i for i in db_dashboard.find(query)]

    index_obj = dindex.DashboardIndexEntry(uid, result[0]["earnings"])
    index_obj.add_new_data(new_data)
    payload = index_obj.return_obj()

    db_dashboard.update_one(query, payload)

    return payload

def generate_report(uid):
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook('Expenses01.xlsx')
    worksheet = workbook.add_worksheet()