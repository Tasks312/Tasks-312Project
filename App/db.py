from flask_pymongo import PyMongo

from flask import current_app, g

import App.bcrypt as bcrypt
import App.game as game

next_post_id = -1
next_game_id = -1

def init_mongo():
    if ('mongo' not in g):
        g.mongo = PyMongo(current_app)
    
    return g.mongo.db

# returns a cursor for a user with that username (or None)
def get_user_by_name(username: str):
    users = init_mongo().users

    return users.find_one({"username": username})

# returns a cursor for a user with that token (or None)
def get_user_by_token(token: str):
    users = init_mongo().users

    return users.find_one({"authtoken": bcrypt.hash_token(token)}) 

# returns a cursor for a user with the auth token from the request cookie (or None)
def get_user_by_request(request):
    token = request.cookies.get("authtoken")
    if (not token):
        return None

    return get_user_by_token(token)

# returns true if request is from an authenticated user
def is_user_authenticated(request):
    return get_user_by_request(request) != None


# returns a cursor for a post with the id
def get_post_by_id(id: int):
    if (id == None):
        return None

    posts = init_mongo().posts
    return posts.find_one({"post_id": id})

def get_all_posts():
    posts = init_mongo().posts
    return posts.find()

# returns a cursor for a game with the id
def get_game_by_id(id: int):
    if (id == None):
        return
    
    games = init_mongo().games
    return games.find_one({"game_id", id})

def get_all_games():
    games = init_mongo().games
    return games.find()

# sorts the post and then returns the highest post_id + 1 
# return 0 if this will be first post in the database
def get_next_post_id():
    global next_post_id

    if (next_post_id == -1):
        all_posts = get_all_posts()

        if(all_posts):
            high_post = all_posts.sort("post_id", -1).limit(1)

            # why a for loop for a list with 1 entry? Because MongoDB and Python...
            for post in high_post:
                highestId = post["post_id"]
                next_post_id = int(highestId)

    next_post_id += 1
    return next_post_id

# identical to get_next_post_id
def get_next_game_id():
    global next_game_id

    if (next_game_id == -1):
        all_games = get_all_games()

        if (all_games):
            high_game = all_games.sort("game_id", -1).limit(1)

            for game in high_game:
                highestId = game["game_id"]
                next_game_id = int(highestId)
    
    next_game_id += 1
    return next_game_id

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

def create_post(username: str, title: str, description: str):
    
    if(not username or not title or not description):
        return None
    
    posts = init_mongo().posts
    
    postId = get_next_post_id()
    postInsertion = posts.insert_one({
        "username": username,
        "title": title,
        "description": description,
        "post_id": int(postId),
        "like_count": 0
    })
    # continue
    return (postInsertion)

# loads a game from the database (if it exists)
def load_game(id: int):
    gamestate = get_game_by_id(id)

    if (gamestate):
        return game.from_obj(gamestate)
    
    return None

# player1 and player2 should be verified before this
def create_game(player1: str, player2: str):
    games = init_mongo().games
    gameId = get_next_game_id()
    
    state = game.Gamestate(gameId, player1, player2)

    games.insert_one(state.as_obj())

    return state

# saves the state of the game to the database
def save_game(gamestate: game.Gamestate):
    games = init_mongo().games

    games.update_one(
    {"game_id": gamestate.id},
        {"$set": gamestate.as_obj()})
