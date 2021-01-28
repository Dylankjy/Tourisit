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

client = pymongo.MongoClient(
    'mongodb://tourisitUser:desk-kun_did_nothing_wrong_uwu@ip.system.gov.hiy.sh:27017')['Tourisit']

# Collections
db_dashboard = client['Dashboard']
db_transactions = client['Transactions']


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


def generate_report(uid, year, month):
    # Generate random string for download file
    raw_sid = ""
    # Using UUID4 to generate random strings
    for i in range(10):
        raw_sid += str(uuid.uuid4())

    # Generate even more random SID by using SHA3-512
    value = hashlib.sha1(raw_sid.encode('utf-8')).hexdigest()

    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(f'tmp_data/{value}.xlsx')
    worksheet = workbook.add_worksheet()

    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0

    query_uid = {
        "tg_uid": ObjectId(uid),
        "month_paid": int(year),
        "year_paid": int(month)
    }

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


# generate_report("5feafbbf4dbad8d4b8614958")

class ReportGenForm(FlaskForm):
    month_filter = StringField(
        'Month',
        [DataRequired()]
    )
    year_filter = StringField(
        'Year',
        [DataRequired()]
    )
