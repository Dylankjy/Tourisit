import auth as auth

# Valid session id, returns object from mongo
print(auth.is_auth('superSecretSessionID'))

# Invalid session id, return False
print(auth.is_auth('hackermanGoBrrrrr'))
