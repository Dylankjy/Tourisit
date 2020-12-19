import hashlib
import smtplib
import ssl
import uuid
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

import bcrypt
import pymongo
from bson import ObjectId
from flask import request

import models.User as User

client = pymongo.MongoClient('mongodb+srv://admin:slapbass@cluster0.a6um0.mongodb.net/test')['Tourisit']
db_sessions = client['Sessions']
db_users = client['Users']
db_listings = client['Listings']
env = client['Environment']

sendgrid_key = [i for i in env.find({})][0]["sendgrid_api"]
template_header = open("email/header.html", "r").read()
template_email_confirmation = open("email/confirmation.html", "r").read()


def create_account(name='Takabaka', raw_password=b'UwUs696969!', email='takabaka69@example.com'):
    # TODO: Change this to dynamic ^^^^^

    # Check whether account already exists
    query = {
        "email": email
    }
    query_result = [i for i in db_users.find(query)]
    if len(query_result) > 0:
        return False

    # Hash password
    hashed_password = bcrypt.hashpw(raw_password, bcrypt.gensalt())

    # Construct an object implements class
    user_obj = User.User(name, hashed_password, email)

    # Get Dictionary for BSON
    user_dict = user_obj.return_obj()

    # Database Ops: Insert user
    db_users.insert_one(user_dict)

    return True


def add_session(uid):
    # Empty string
    raw_sid = ""

    # Using UUID4 to generate random strings
    for i in range(10):
        raw_sid += str(uuid.uuid4())

    # Generate even more random SID by using SHA3-512
    hashed_sid = hashlib.sha3_512(raw_sid.encode('utf-8')).hexdigest()

    # Dictionary for BSON
    session_dict = {
        "sid": hashed_sid,
        "uid": ObjectId(uid)
    }

    # Database Ops: Insert into session
    db_sessions.insert_one(session_dict)

    return hashed_sid


def login_account(email='takabaka69@example.com', password=b'UwUs696969!'):
    # TODO: Change this to dynamic ^^^^^

    # Get user data from db by email
    query = {
        "email": email
    }
    query_result = [i for i in db_users.find(query)][0]

    if not bcrypt.checkpw(password, query_result["password"]):
        return False

    return add_session(query_result["_id"])


def logout_account(sid):
    # Get session from database
    query = {
        "sid": sid
    }
    query_result = [i for i in db_sessions.find(query)]
    if len(query_result) == 1:
        db_sessions.delete_one(query)
        return True
    else:
        return False


def delete_account(uid):
    try:
        # Query everything in relation to UID
        query = {
            '$or': {
                "_id": ObjectId(uid),
                "uid": ObjectId(uid),
                'tg_uid': ObjectId(uid),
                'cust_uid': ObjectId(uid)
            }
        }

        # Yeet everything into oblivion
        db_users.delete_many(query)
        db_sessions.delete_many(query)
        db_listings.delete_many(query)

        return True
    except:
        return Exception("Couldn't yeet user account due to an error.")


def send_confirmation_email():
    port = 465  # For SSL
    password = sendgrid_key

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Email headers
    message = MIMEMultipart("alternative")
    message["Subject"] = "Tourisit - Confirm your Email"
    message["From"] = formataddr((str(Header('Tourisit', 'utf-8')), 'notifications@tourisit.ichiharu.com'))
    message["To"] = "tenkotofu@gmail.com"

    code = 'https://tourisit.ichiharu.com/confirmEmail/code'

    # Build email HTML from 2 parts. Format with URL
    content = template_header + template_email_confirmation.format(
        confirmation_url=code)

    # Add content to email
    message.attach(MIMEText(content, "html"))

    # Send email
    with smtplib.SMTP_SSL("smtp.sendgrid.net", port, context=context) as server:
        server.login("apikey", password)
        server.sendmail(
            "notifications@tourisit.ichiharu.com", "tenkotofu@gmail.com", message.as_string()
        )


def get_sid():
    try:
        # Get SID
        sid = request.cookies.get('sid')
        return sid
    except:
        return None


def is_auth(gib_data=False):
    if get_sid() is not None:
        req_sid = get_sid()
    else:
        return False

    query = {
        "sid": req_sid
    }

    try:
        query_result = [i for i in db_sessions.find(query)]
        if len(query_result) == 1:
            if gib_data:
                query_user = {"_id": ObjectId(query_result[0]['uid'])}
                query_user_data = [i for i in db_users.find(query_user)]

                user_data = {
                    "name": query_user_data[0]['name'],
                    "email": query_user_data[0]['email']
                }
                return user_data
            elif not gib_data:
                return True
        else:
            return False
    except:
        raise Exception('auth.py: Cannot authenticate user due to an unknown error')
