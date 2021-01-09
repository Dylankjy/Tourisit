import pymongo

# MongoDB connection string
client = pymongo.MongoClient('mongodb://tourisitUser:desk-kun_did_nothing_wrong_uwu@ip.system.gov.hiy.sh:27017')['Tourisit']

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


