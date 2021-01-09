from datetime import datetime

import bson
import pymongo
# MongoDB connection string
from bson import ObjectId
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

client = pymongo.MongoClient('mongodb://tourisitUser:desk-kun_did_nothing_wrong_uwu@ip.system.gov.hiy.sh:27017')['Tourisit']

import models.Chat as Chat

# Collections
db_users = client['Users']
db_sessions = client['Sessions']
db_chats = client['Chats']

test_sid = "b687c32ba5cbcde4ddb20504d832a0e7857cbff22bd6df1137097a78f0752" \
           "060ab64074de7acc8933c073f219fe30f62044bb1618e798e1d77703bfaf15827cd"

test_sid2 = '9d1c1cff7e66b604cc8df66a075e61fcd239a1fc5154def7964bf87ea99772f13e' \
            '7886d986180bab9194e9bd089d2cb364a3f8fc22e5ff68a97c3e7a1b928327'


def create_chat_room(participants, is_booking_chat):
    if is_booking_chat:
        # Set type to Booking mode
        chat_type = "BOOKING"
    elif not is_booking_chat:
        # Set type to User with User mode (UwU)
        chat_type = "UwU"
    else:
        return Exception(f"Invalid chat mode of {is_booking_chat}")

    # Initialise empty list
    participants_bson = []

    # Convert all UIDs into BSON ObjectId
    for i in range(len(participants)):
        participants_bson.append(ObjectId(participants[i]))

    chat_obj = Chat.ChatRoom(participants_bson, chat_type)
    chat_dict = chat_obj.return_obj()

    # Database Ops: Insert chatroom dict
    inserted_dict = db_chats.insert_one(chat_dict)

    # Return chatroom id
    return inserted_dict.inserted_id


# create_chat_room(["5feafbbf4dbad8d4b8614958", "5feec7b2adbcd32780a3a758"], True)
# create_chat_room(["5feafbbf4dbad8d4b8614958", "5fec8a85b11a8931d7656f06"], False)

def get_chat_list_for_ui(sid, chat_type):
    # Query SID
    query_sid = {
        "sid": sid
    }

    # Find sender uid by sid
    try:
        uid = [i for i in db_sessions.find(query_sid)][0]["uid"]
    except IndexError:
        return False

    # Query to find all chats of user
    query_uid_in_chats = {
        '$and': [
            {
                'participants': {
                    "$in": [uid]
                }
            }
        ]
    }

    if chat_type != 'ALL':
        query_uid_in_chats['$and'].append({
            'chat_type': chat_type
        })

    # Get list of chat messages from database
    list_of_chats = [i for i in db_chats.find(query_uid_in_chats)]

    # Initialised variables
    compiled_list = []

    # Get recipient's uid
    for i in range(len(list_of_chats)):
        for u in range(len(list_of_chats[i]["participants"])):
            if list_of_chats[i]["participants"][u] != uid:
                recipient_uid = list_of_chats[i]["participants"][u]
                chat_type = list_of_chats[i]['chat_type']
                chat_room_id = list_of_chats[i]['_id']

                query_recipient_uid = {
                    "_id": recipient_uid
                }

                recipient_name = [a for a in db_users.find(query_recipient_uid)][0]["name"]

                compiled_list.append(
                    {"id": chat_room_id, "name": recipient_name, "uid": recipient_uid, "chat_type": chat_type})

    return compiled_list


# get_chat_list(test_sid, "ALL")


def get_chat_room(sid, chat_id):
    # Query SID
    query_sid = {
        "sid": sid
    }

    # Find sender uid by sid
    try:
        uid = [i for i in db_sessions.find(query_sid)][0]["uid"]
    except IndexError:
        return False

    try:
        # Query to find specific chat user is wanting to push message into
        query_uid_in_chats = {
            '$and': [
                {
                    '_id': ObjectId(chat_id)
                },
                {
                    'participants': {
                        "$in": [uid]
                    }
                }
            ]
        }
    except bson.errors.InvalidId:
        return False

    # Get list of chat messages from database
    try:
        chatroom_data = [i for i in db_chats.find(query_uid_in_chats)][0]
    except IndexError:
        return False

    # Initialised variables
    compiled_chat_room = []
    list_of_participant_names = []

    for u in chatroom_data["participants"]:
        query_uid_get_participants = {
            "_id": u
        }

        user_name = [a for a in db_users.find(query_uid_get_participants)][0]["name"]

        if user_name not in list_of_participant_names:
            list_of_participant_names.append(user_name)

    try:
        for i in range(len(chatroom_data["messages"])):
            query_uid_get_participants = {
                "_id": chatroom_data["messages"][i]['sender_id']
            }

            if chatroom_data["messages"][i]['sender_id'] != uid:
                is_self = False
            else:
                is_self = True

            message = chatroom_data["messages"][i]['msg_content']
            user_name = [a for a in db_users.find(query_uid_get_participants)][0]["name"]

            compiled_chat_room.append(
                {"sender_name": user_name, "uid": query_uid_get_participants, "msg_content": message, "self": is_self}
            )
    except IndexError:
        pass

    return {"chatroom": compiled_chat_room, "names": ' ↔ '.join(list_of_participant_names)}


# print(get_chat_room(test_sid, "5fef54775c7ba372a70fa0b0"))


def add_message(chat_id, sender_sid, message):
    # Query SID
    query_sid = {
        "sid": sender_sid
    }

    # Find sender uid by sid
    try:
        sender_uid = [i for i in db_sessions.find(query_sid)][0]["uid"]
    except IndexError:
        return False

    # Query to find specific chat user is wanting to push message into
    query_uid_in_chats = {
        '$and': [
            {
                '_id': ObjectId(chat_id)
            },
            {
                'participants': {
                    "$in": [sender_uid]
                }
            }
        ]
    }

    # Get data for Chat room from UID in participants
    chat_room_data = [i for i in db_chats.find(query_uid_in_chats)]

    # Security check: Return false if participant doesn't appear in queries
    if len(chat_room_data) != 1:
        return False
    else:
        # Generate timestamp in ISO format
        date = datetime.now()
        current_timestamp = date.isoformat()

        # Create object implements Message
        chat_message_obj = Chat.Message(sender_uid, current_timestamp, message)
        chat_message_dict = chat_message_obj.return_obj()

        # Query chat room by ID
        query_chat_room = {
            '_id': ObjectId(chat_id)
        }

        # Payload to push into database
        payload = {
            '$push':
                {
                    "messages": chat_message_dict
                }
        }

        # Database Ops: Update records with message
        db_chats.update_one(query_chat_room, payload)

        return True


# add_message("5ff0b727041631a155c77dea", test_sid, "I want to book this")

class ChatForm(FlaskForm):
    message = StringField(
        'Chat',
        [DataRequired()]
    )
