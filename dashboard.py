import hashlib
import uuid
from datetime import datetime

import pymongo
import xlsxwriter

# MongoDB connection string
from bson import ObjectId
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

import models.DashboardIndex as dindex

from statistics import mean

client = pymongo.MongoClient(
    'mongodb://tourisitUser:desk-kun_did_nothing_wrong_uwu@ip.system.gov.hiy.sh:27017')['Tourisit']

# Collections
db_dashboard = client['Dashboard']
db_transactions = client['Transactions']
db_shop = client['Listings']


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


def get_earning_breakdown(uid):
    """
    Get earnings from database per month
    :param uid: Target user's ID
    :return: Data per month in a list
    """

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

    if len(transactions) != 6:
        for _ in range(6 - len(transactions)):
            transactions.insert(0, {'total': 0})

    return transactions


def get_satisfaction_rate(uid):
    """
    Get satisfaction rate from database per month
    :param uid: Target user's ID
    :return: Data per month in a list
    """

    x = list(db_shop.find({"tg_uid": ObjectId(uid), "tour_reviews": {"$ne": "null"}}, {"_id": 0, "tour_reviews": 1}))
    x = [x[i] for i in range(len(x)) if len(x[i]['tour_reviews']) != 0]
    l = []
    for listing in x:
        # print(listing)
        d = {}
        for review in listing['tour_reviews']:
            # print(review)
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

    if len(l) != 6:
        for _ in range(6 - len(l)):
            l.insert(0, {'stars': 0})

    return l


# print(get_earning_breakdown("600666f7ccab3b102fce39fb"))


def generate_report(uid, year=None, month=None):
    """
    Generate a new xlsx file as report for download
    :param uid: Target user's ID
    :param year: (Optional) Filter for year
    :param month: (Optional) Filter for month
    :return: Report's file name
    """

    # Check whether filter is empty
    if year is None or month is None:
        query_uid = {
            "tg_uid": ObjectId(uid),
        }
    else:
        query_uid = {
            "tg_uid": ObjectId(uid),
            "month_paid": int(month),
            "year_paid": int(year)
        }

    # Generate random string for download file
    raw_sid = ""
    # Using UUID4 to generate random strings
    for i in range(10):
        raw_sid += str(uuid.uuid4())

    # Generate even more random SID by using SHA3-512
    generated_filename = hashlib.sha1(raw_sid.encode('utf-8')).hexdigest()

    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(f'tmp_data/{generated_filename}.xlsx')
    worksheet = workbook.add_worksheet()

    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0

    data_for_input = [
        ['Listing Name', 'Timestamp', 'Total Earned', 'Payment Status']
    ]

    # Get all in relates to UID from Transaction database
    transactions = [i for i in db_transactions.find(query_uid)]

    for transaction in transactions:
        # query_listing_for_name = {
        #     "tour_name": transaction['']
        # }

        listing_name = str(transaction['booking'])

        date_paid = datetime.fromisoformat(transaction["date_paid"]).strftime('%d %B %Y @ %X')

        if transaction['pay_status'] == 0:
            pay_status = "Pending"
        else:
            pay_status = "Completed"

        data_for_input.append(
            [listing_name, date_paid, float(transaction["earnings"]), pay_status]
        )

    for listing_name, timestamp, total_payable, payment_status in data_for_input:
        worksheet.write(row, col, listing_name)
        worksheet.write(row, col + 1, timestamp)
        worksheet.write(row, col + 2, total_payable)
        worksheet.write(row, col + 3, payment_status)
        row += 1

    # Write a total using a formula.
    worksheet.write(row, 0, 'Total')
    worksheet.write(row, 2, '=SUM(C2:C{bottom})'.format(bottom=row))

    workbook.close()

    return generated_filename


# generate_report("5feafbbf4dbad8d4b8614958")

class ReportGenForm(FlaskForm):
    """
    (FRONTEND, WTForm) For generation of report
    """
    date_filter = StringField(
        'Date Scope'
    )
