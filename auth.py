import pymongo
from bson import ObjectId

client = pymongo.MongoClient('mongodb+srv://admin:slapbass@cluster0.a6um0.mongodb.net/test')['Tourisit']
db_sessions = client['Sessions']
db_users = client['Users']


def is_auth(req_sid):
    query = {
        "sid": req_sid
    }
    try:
        query_result = [i for i in db_sessions.find(query)]

        if len(query_result) == 1 and req_sid != '' and req_sid is not None:
            query_user = {"_id": ObjectId(query_result[0]['uid'])}
            user_data = [i for i in db_users.find(query_user)]

            return user_data[0]
        else:
            return False
    except:
        raise Exception('auth.py: Cannot authenticate user due to an unknown error')
