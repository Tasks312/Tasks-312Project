from flask_pymongo import PyMongo

from flask import current_app, g

import App.bcrypt as bcrypt

def init_mongo():
    if ('mongo' not in g):
        g.mongo = PyMongo(current_app)
    
    return g.mongo.db

# returns a cursor for a user with that username (or None)
def get_user_by_name(username: str):
    users = init_mongo().users

    return users.find_one({"username": username})

# returns a cursor for a user with the auth token from the request cookie (or None)
def get_user_by_request(request):
    username = request.cookies.get("username")
    if (not username):
        return None
    
    puser = get_user_by_name(username)
    if (not puser):
        return None
    
    token = request.cookies.get("authtoken")
    if (not token):
        return None
    
    if (bcrypt.hash_compare(puser["authtoken"], token)):
        return puser
    
    return None

def get_user_by_token(request):
    users = init_mongo().users
    token = request.cookies.get("authtoken")
    if(token):
        return users.find_one({"authtoken": bcrypt.hash_token(token)}) 
    
    return None

# returns true if request is from an authenticated user
def is_user_authenticated(request):
    return get_user_by_request(request) != None

# returns a tuple of (token, error). token is None on error
# this is the unencrypted token so the cookie can be set
def register(username: str, password: str):
    if (not username):
        return "No username"
    elif (not password):
        return "No password"

    username = bcrypt.escape_html(username)

    users = init_mongo().users

    if (get_user_by_name(username)):
        return "Username already in use"

    users.insert_one({
        "username": username,
        "password": bcrypt.hash(password)
    })

    return None

def login(username: str, password: str):
    if (not username):
        return (None, "No username")
    elif (not password):
        return (None, "No password")
    
    username = bcrypt.escape_html(username)
    
    user = get_user_by_name(username)
    if (user):
        hash = user['password']# The hashed passsword fromreturn users.find_one({"username": username})
        compare = bcrypt.hash_compare(hash,password)
        if(not compare):
            return(None, "Incorrect Username/Password")
        
        token = bcrypt.gen_token()
        users = init_mongo().users

        users.update_one({"username": username},
        {"$set":{
            "username": username,
            "password": bcrypt.hash(password),
            "authtoken" : bcrypt.hash_token(token)
        }})

        return (token, None)
    
    return (None, "No such user")