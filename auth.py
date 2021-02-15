import hashlib
import smtplib
import ssl
import uuid
from datetime import datetime
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

import bcrypt
import pymongo
from bson import ObjectId
from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Email

import models.User as User

# MongoDB connection string
client = pymongo.MongoClient(
    'mongodb://tourisitUser:desk-kun_did_nothing_wrong_uwu@ip.system.gov.hiy.sh:27017')['Tourisit']

# Collections
env = client['Environment']
db_users = client['Users']
db_sessions = client['Sessions']
db_tokens = client['Tokens']
db_listings = client['Listings']

# Email Templates & API Key
try:
    sendgrid_key = [i for i in env.find({})][0]["sendgrid_api"]
    template_header = open("email/header.html", "r").read()
except BaseException:
    print("Check your network connectivity. Couldn't contact MongoDB database! Are you using the school network?")
    exit(0)

# Template: Confirmation
template_email_confirmation = open("email/confirmation.html", "r").read()
# Template: Password reset
template_password_reset = open("email/pwdreset.html", "r").read()


def create_account(name, raw_password, email):
    """
    Used to create an account. Takes in User class and returns into database
    :param name: User's name
    :param raw_password: User's password (in plain text)
    :param email: User's Email Address
    :return: Status of account creation
    """

    # Convert password into byte literals
    password = raw_password.encode('utf-8')

    # Check whether account already exists
    query = {
        "email": email
    }
    query_result = [i for i in db_users.find(query)]
    if len(query_result) > 0:
        return False

    # Hash password
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

    # Construct an object implements User class
    user_obj = User.User(name, hashed_password, email)

    # Get Dictionary for BSON
    user_dict = user_obj.return_obj()

    # Database Ops: Insert user
    db_users.insert_one(user_dict)

    # Automatically send confirmation email to user
    send_confirmation_email(None, email)

    return True


# create_account("Takahashi Yamaro", "HelloWorld123", "takahashi@example.com")


def add_session(uid):
    """
    Add a new session for persisting logins.
    :param uid: Target User ID
    :return: Session ID
    """
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


def add_token(token_type, uid):
    """
    For adding confirmation tokens & password change tokens.
    :param token_type: Type of token to generate
    :param uid: Target User ID
    :return: Generated token value
    """
    # token_type valid values
    # - email_verification
    # - password_reset

    # Empty string
    raw_sid = ""

    # Using UUID4 to generate random strings
    for _ in range(10):
        raw_sid += str(uuid.uuid4())

    # Generate even more random SID by using SHA3-512
    token_value = hashlib.sha3_512(raw_sid.encode('utf-8')).hexdigest()

    # Query for finding all tokens of same type with uid
    query_for_deletion_tokens = {
        "uid": ObjectId(uid),
        "type": token_type
    }

    # Database Ops: Delete any preexisting tokens of same type
    db_tokens.delete_many(query_for_deletion_tokens)

    # Dictionary for BSON
    token_dict = {
        "type": token_type,
        "token": token_value,
        "uid": ObjectId(uid)
    }

    # Database Ops: Insert into session
    db_tokens.insert_one(token_dict)

    return token_value


# print(add_token("phone_verification", "5fe8c3fe1fb459db658e6d4e"))


def verify_remove_token(token_type, token, check_only=False):
    """
    Verify and remove tokens
    :param token_type: Type of token to validate
    :param token: Token value
    :param check_only:
    :return: Status of verification
    """

    # Prevent database exploit by rejecting blank entries
    if token is None or token == "":
        return False

    # Query to check token's existence
    query_for_token = {
        "token": token,
        "type": token_type
    }

    # Database Ops: Get list of tokens with query
    query_result = [i for i in db_tokens.find(query_for_token)]

    # Pre-initialise payload for later use
    payload = None

    # Do if exist
    if len(query_result) == 1:
        if token_type == "email_verification":
            payload = {
                "$set": {
                    "email_status": True
                }
            }

            # Query account from database
            query_for_account = {
                "_id": ObjectId(query_result[0]["uid"])
            }

            # Database Ops: Update status
            db_users.update_one(query_for_account, payload)

        if token_type == "password_reset" and check_only:
            return True

        # Query select any preexisting tokens
        query_for_deletion_tokens = {
            "uid": ObjectId(query_result[0]["uid"]),
            "type": token_type
        }

        # Database Ops: Delete any existing tokens of same type
        db_tokens.delete_many(query_for_deletion_tokens)

        return True


def login_account(email, unencoded_password):
    """
    Authenticate and login to account.
    :param email: User's Email address
    :param unencoded_password: User's supposed incoming password (unencoded)
    :return: Authentication status
    """
    password = unencoded_password.encode('utf-8')

    # Get user data from db by email
    query = {
        "email": email.lower()
    }

    try:
        query_result = [i for i in db_users.find(query)][0]

        if not bcrypt.checkpw(password, query_result["password"]):
            return False

        if query_result["email_status"] is False:
            return "UNVERIFIED"

        # Generate timestamp in ISO format
        date = datetime.now()
        current_timestamp = date.isoformat()

        # Set last seen
        payload = {
            '$set': {
                "last_seen_time": current_timestamp
            }
        }

        # Database Ops: Update last seen
        db_users.update_one(query, payload)

        return add_session(query_result["_id"])
    except IndexError:
        return False


def get_user_id(sid):
    """
    Get User's ID from the current session
    :param sid: Target user's current session ID
    :return: User's ID
    """
    # Find UID from SID
    query = {
        "sid": sid
    }
    query_result = [i for i in db_sessions.find(query)]

    # Get UID
    if len(query_result) == 1:
        uid = query_result[0]["uid"]
        return uid
    else:
        return False


def logout_account(sid, all_sessions=False):
    """
    Clear session(s) for logout
    :param sid: Current session ID
    :param all_sessions: Option to logout of all sessions
    :return: Status of logout
    """
    # Get session from database
    query = {
        "sid": sid
    }

    if not all_sessions:
        query_result = [i for i in db_sessions.find(query)]
        if len(query_result) == 1:
            db_sessions.delete_one(query)
            return True

        return False
    elif all_sessions:
        query_result = [i for i in db_sessions.find(query)]

        query_all_sessions = {
            "uid": ObjectId(query_result[0]['uid'])
        }
        if len(query_result) == 1:
            db_sessions.delete_many(query_all_sessions)

            return True

        return False


def delete_account(uid):
    """
    Delete a user account using UID (WARNING! THERE IS NO AUTH CHECKS)
    :param uid: Target User's ID
    :return: Returns True when DB operation is completed
    """
    try:
        # Query everything in relation to UID
        query = {
            # '$or': {
            "_id": ObjectId(uid)
            # "uid": ObjectId(uid),
            # 'tg_uid': ObjectId(uid),
            # 'cust_uid': ObjectId(uid)
            # }
        }

        # Yeet everything into oblivion
        db_users.delete_one(query)
        # db_sessions.delete_many(query)
        # db_listings.delete_many(query)

        print('OK')

        return True
    except BaseException:
        return Exception("Couldn't yeet user account due to an error.")


def send_confirmation_email(email_type, user_email):
    """
    Uses SMTP (via SendGrid) to send emails.
    :param email_type: Type of email to send
    :param user_email: Target user's email
    :return: Status of operation
    """

    # Query user's email
    query = {
        "email": user_email
    }

    # Query result for UID
    user_obj = [i for i in db_users.find(query)]
    uid = user_obj[0]["_id"]

    port = 465  # For SSL
    password = sendgrid_key

    # Create a secure SSL context
    context = ssl.create_default_context()

    message = MIMEMultipart("alternative")

    if email_type == "email_verification":
        # Email headers
        message["Subject"] = "Tourisit - Confirm your Email"
        message["From"] = formataddr(
            (str(Header('Tourisit', 'utf-8')), 'notifications@tourisit.hiy.sh'))
        message["To"] = user_email

        code = 'https://tourisit.hiy.sh/endpoint/email_confirmation?token=' + \
               add_token("email_verification", uid)

        # Build email HTML from 2 parts. Format with URL
        content = template_header + template_email_confirmation.format(
            confirmation_url=code)

        # Add content to email
        message.attach(MIMEText(content, "html"))
    elif email_type == "password_reset":
        if len(user_obj) != 1:
            # print(user_obj)
            return False

        # Email headers
        message["Subject"] = "Tourisit - Password reset"
        message["From"] = formataddr(
            (str(Header('Tourisit', 'utf-8')), 'notifications@tourisit.hiy.sh'))
        message["To"] = user_email

        code = 'https://tourisit.hiy.sh/login/recover_account/reset?token=' + \
               add_token("password_reset", uid)

        # Build email HTML from 2 parts. Format with URL
        content = template_header + template_password_reset.format(
            reset_url=code)

        # Add content to email
        message.attach(MIMEText(content, "html"))

    # Send email
    with smtplib.SMTP_SSL("smtp.sendgrid.net", port, context=context) as server:
        server.login("apikey", password)
        server.sendmail(
            "notifications@tourisit.hiy.sh",
            user_email,
            message.as_string())

    return True


def get_sid():
    """
    Get current session ID of user
    :return: Session ID
    """
    try:
        # Get SID
        sid = request.cookies.get('tourisitapp-sid')
        return sid
    except BaseException:
        return None


def is_auth(gib_data=False, gib_password=False):
    """
    Check current session is valid.
    :param gib_data: Make return statement into an accessor method
    :param gib_password: Make return statement return password when accessor method is True
    :return: Either status of session or accessor result
    """
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

                user_data = query_user_data[0]
                if not gib_password:
                    del user_data['password']
                del user_data['stripe_id']

                return user_data
            elif not gib_data:
                return True
        else:
            return False
    except BaseException:
        raise Exception(
            'auth.py: Cannot authenticate user due to an unknown error')


def generate_password_hash(raw_password):
    """
    For use for changing password
    :param raw_password: User's new password
    :return:
    """
    # Encode password in byte literals
    password = raw_password.encode('utf-8')

    # Hash password using bcrypt
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

    return hashed_password


def check_password_correlate(raw_incoming_password, current_password_hash):
    """
    To compare old hash to new password (unencoded). For use during password changes.
    :param raw_incoming_password: Incoming password (unencoded)
    :param current_password_hash: Current password hash
    :return: Status of password correlation
    """
    # Encode password in byte literals
    incoming_password = raw_incoming_password.encode('utf-8')

    # Check whether passwords match
    if not bcrypt.checkpw(incoming_password, current_password_hash):
        return False

    return True


class SignupForm(FlaskForm):
    full_name = StringField(
        'Full Name',
        [DataRequired()]
    )
    email = StringField(
        'Email Address',
        [DataRequired(), Email()]
    )
    password = StringField(
        'Password',
        [DataRequired()]
    )


class SelectAccModeForm(FlaskForm):
    acc_mode = SelectField(
        'acc_mode',
        choices=[(0, 'Tourist'), (1, 'Tour Guide')]
    )


class LoginForm(FlaskForm):
    email = StringField(
        'Email Address',
        [DataRequired(), Email()]
    )
    password = StringField(
        'Password',
        [DataRequired()]
    )


class RecoverAccountForm(FlaskForm):
    email = StringField(
        'Email Address',
        [DataRequired(), Email()]
    )


class PasswordReset(FlaskForm):
    password = StringField(
        'New password',
        [DataRequired()]
    )


class ResendEmailForm(FlaskForm):
    email = StringField(
        'system email'
    )
