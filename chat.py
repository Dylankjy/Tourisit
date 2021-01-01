from datetime import datetime

import pymongo

# MongoDB connection string
from bson import ObjectId

client = pymongo.MongoClient('mongodb+srv://admin:slapbass@cluster0.a6um0.mongodb.net/test')['Tourisit']

import models.Chat as Chat

# Collections
db_users = client['Users']
db_sessions = client['Sessions']
db_chats = client['Chats']


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

    db_chats.insert_one(chat_dict)

    return True

# create_chat_room(["5feafbbf4dbad8d4b8614958", "5fec8a85b11a8931d7656f06"], True)


def add_message(chat_id, sender_sid, message):
    # Query SID
    query_sid = {
        "sid": sender_sid
    }

    try:
        sender_uid = [i for i in db_sessions.find(query_sid)][0]["uid"]
    except IndexError:
        return False

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

        chat_message_obj = Chat.Message(sender_uid, current_timestamp, message)
        chat_message_dict = chat_message_obj.return_obj()

        query_chat_room = {
            '_id': ObjectId(chat_id)
        }

        payload = {
            '$push':
                {
                    "messages": [chat_message_dict]
                }
        }

        db_chats.update_one(query_chat_room, payload)
        return True
