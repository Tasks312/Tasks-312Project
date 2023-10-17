from flask_pymongo import PyMongo

from flask import current_app, g

import App.bcrypt as bcrypt

def init_mongo():
    if ('mongo' not in g):
        g.mongo = PyMongo(current_app)
    
    return g.mongo

# returns a cursor for a user with that username (or None)
def get_user_by_name(username: str):
    users = init_mongo().users

    return users.find_one({"username": username})

# returns a cursor for a user with that raw token (or None)
def get_user_by_token(token: str):
    users = init_mongo().users

    return users.find_one({"authtoken": bcrypt.hash(token)}) 

# returns a tuple of (token, error). token is None on error
# this is the unencrypted token so the cookie can be set
def register(username: str, password: str):
    if (not username):
        return (None, "No username")
    elif (not password):
        return (None, "No password")

    users = init_mongo().users

    if (get_user_by_name(username)):
        return (None, "Username already in use")

    token = bcrypt.gen_token()
    users.insert_one({
        "username": username,
        "password": bcrypt.hash(password),
        "authtoken" : bcrypt.hash(token)
    })

    return (token, None)
