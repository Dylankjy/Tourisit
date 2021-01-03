import pymongo

# MongoDB connection string
client = pymongo.MongoClient('mongodb+srv://admin:slapbass@cluster0.a6um0.mongodb.net/test')['Tourisit']

# Collections
env = client['Environment']
db_users = client['Users']
db_sessions = client['Sessions']
db_tokens = client['Tokens']
db_listings = client['Listings']


def list_user_accounts():
    # Wildcard query
    wildcard_query = {}

    query_result = [i for i in db_users.find(wildcard_query)]

    return query_result


def list_listings():
    # Wildcard query
    wildcard_query = {}

    query_result = [i for i in db_listings.find(wildcard_query)]

    return query_result


