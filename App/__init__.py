from flask import Flask, redirect, request, make_response, render_template, jsonify
import os, threading, json

import App.db as db
import App.bcrypt as bcrypt

def strToInt(string: str):
    if (string is None):
        return None

    try:
        return int(string)
    except:
        return None

def create_app(test_config = None):
    app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb://mongo:27017/database"
    app.config["SECRET_KEY"] = 'secrete' #idk will need to change this
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/")
    def index():
        user = db.get_user_by_request(request)
        if(user):
            profile = db.get_profile_picture(user)

            if ("lobby_id" in user):
                game = db.load_game(user["lobby_id"])
                if (game and not game.is_over()):
                    other_player = game.p2 if game.p1 == user["username"] else game.p1

                    other_profile = db.get_profile_picture_from_username(other_player)

                    p1_pic = profile if game.p1 == user["username"] else other_profile
                    p2_pic = profile if game.p2 == user["username"] else other_profile
                    winner = game.winner if game.is_over() else None

                    return render_template("board.html", p1=game.p1, p2=game.p2, p1_pic=p1_pic, p2_pic=p2_pic, winner=winner)

                lobby = db.load_lobby("lobby_id")
                # do something special if in a lobby?

            return render_template("lobby.html", logged_username= user["username"], profile_picture=profile)

        return render_template("Authentication.html")

    @app.route("/profile-pic", methods=["POST"])
    def uploadProfilePic():
        user = db.get_user_by_request(request)
        if not user:
            response = make_response(redirect("/"), "unauthorized")
            response.status_code = 401
            return response

        err = db.insert_profile_picture(user["username"], request)
        if (err):
            response = make_response(redirect("/"), err)
            response.status_code = 400
            return response

        response = make_response(redirect("/"),"OK")
        response.status_code = 301
        return response

    @app.route("/create-lobby", methods=["POST"])
    def createLobby():

        user = db.get_user_by_request(request)
        if (not user):
            response = make_response(redirect("/"), "Unauthorized")
            response.status_code = 401
            return response

        lobby_title = bcrypt.escape_html(request.form["lobby_title"])
        lobby_description = bcrypt.escape_html(request.form["lobby_description"])

        err = db.create_lobby(lobby_title, lobby_description, user)

        if (err):
            response = make_response(redirect("/"), err)
            response.status_code = 400
            return response

        response = make_response(redirect("/"),"OK")
        response.status_code = 301
        return response
    
    @app.route("/join-lobby/<lobby_id>", methods=["POST"])
    def join_lobby(lobby_id = None ):
        lobby_id = strToInt(lobby_id)
        user = db.get_user_by_request(request)
        if not user:
            response = make_response("unauthorized")
            response.status_code = 401
            return response

        lobby = db.load_lobby(lobby_id)

        if not lobby:
            response = make_response("lobby does not exist")
            response.status_code = 401
            return response

        if (not db.join_lobby(user, lobby)):
            response = make_response("cannot join game")
            response.status_code = 401
            return response

        db.save_lobby(lobby)

        game = db.load_game(lobby_id)
        if game:
            game.p2 = user["username"]
            db.save_game(game)
            response = make_response(redirect("/", "OK"))
            response.status_code = 301
            return response

        game = db.create_game(lobby.users[0], lobby.users[1])
        game.id = lobby.id
        db.save_game(game)

        # response = make_response(redirect("/board/"+ str(lobby_id)), "OK") 
        # response.status_code = 301
        # return response
        response = make_response(redirect("/","OK"))
        response.status_code = 301
        return response
    
    @app.route("/lobby-list")
    def lobby_list():

        lobbys = db.get_all_lobbys()

        lobbyJSON = []

        for lobby in lobbys:
            lobbyJSON.append({
                "lobby_id": lobby["lobby_id"],
                "lobby_title": lobby["lobby_title"],
                "lobby_description": lobby["lobby_description"],
            })

        return jsonify(lobbyJSON)

    @app.route("/board/<game_id>")
    def board(game_id = None):
        # note that any user can look at a board, just not participate

        game_id = strToInt(game_id)
        user = db.get_user_by_request(request)
        if not user:
            response = make_response(redirect("/"), "unauthorized")
            response.status_code = 401
            return response
        
        game = db.load_game(game_id)
        if not game:
            response = make_response(redirect("/"), "Game Not Found")
            response.status_code = 404
            return response

        return jsonify(game.as_JSON())
    
    @app.route("/column-position/<column>", methods=["POST"])
    def placeChip(column = None):
        column = strToInt(column)

        user = db.get_user_by_request(request)
        if not user or "lobby_id" not in user:
            response = make_response(redirect("/"), "unauthorized")
            response.status_code = 401
            return response
        
        game = db.load_game(user["lobby_id"])
        if not game:
            response = make_response(redirect("/"), "Game Not Found")
            response.status_code = 404
            return response
        

        if (game.get_turn_player() == user["username"]):
            err = game.try_turn(column)
            db.save_game(game)

            # @TODO something if error?
        
        return jsonify(game.as_JSON())

    @app.route("/register", methods=["POST"])
    def register():
        username = request.form["username_reg"]
        password = request.form["password_reg"]

        err = db.register(username, password)

        if (err):
            response = make_response(err)
            response.status_code = 400
            return response

        response = make_response(redirect("/"),"OK")
        response.status_code = 301
        return response

    @app.route("/login", methods=["POST"])
    def login():
        username = request.form["username_login"]
        password = request.form["password_login"]

        token, err = db.login(username, password)

        if (err):
            response = make_response(err)
            response.status_code = 400
            return response

        response = make_response(redirect("/"), "OK")
        response.status_code = 301
        response.set_cookie("authtoken", token, max_age=36000, httponly = True)
        return response

    @app.route("/logout", methods=["POST"])
    def logout():
        response = make_response(redirect("/"), "OK")
        response.status_code = 301
        response.set_cookie("authtoken", "_logged_out_", max_age=1, httponly = True)
        return response

    @app.route("/create_post", methods=["POST"])
    def createPost():
        title = bcrypt.escape_html(request.form["title"])
        description = bcrypt.escape_html(request.form["description"])

        user = db.get_user_by_request(request)
        if not user:
            response = make_response(redirect("/"), "unauthorized")
            response.status_code = 401
            return response

        postInsert = db.create_post(user["username"], title, description)
        response = make_response(redirect("/"), "OK")
        response.status_code = 301
        return response

    @app.route("/post-history")
    def postHistory():
        posts = db.get_all_posts()

        postJSON = []

        for post in posts:
            postJSON.append({
                "username": post["username"],
                "title": post["title"],
                "description": post["description"],
                "post_id": post["post_id"],
                "like_count": post["like_count"]
            })

        return jsonify(postJSON)


    @app.route("/like-post/<postID>", methods=["POST"])
    def like(postID = None):
        user = db.get_user_by_request(request)
        if (not user):
            response = make_response("Must be logged in to like posts.")
            response.status_code = 403
            return response

        post = db.get_post_by_id(strToInt(postID))
        #print(strToInt(post), flush=True)
        if (not post):
            response = make_response("Post does not exist.")
            response.status_code = 404
            return response

        username = user["username"]
        if username in post.get("liked_by", []):
            return jsonify({"error": "User has already liked this post"}), 400

        liked_by_updated = post.get("liked_by", []) + [username]
        like_count = post["like_count"] + 1

        posts = db.init_mongo().posts
        posts.update_one({"post_id": strToInt(postID)}, {"$set": {"like_count": like_count, "liked_by": liked_by_updated}})

        return jsonify({"message": "Post liked successfully", "likes": like_count + 1}), 200

    @app.route("/unlike-post/<postID>", methods=["POST"])
    def unlike(postID = None):
        user = db.get_user_by_request(request)
        if (not user):
            response = make_response("Must be logged in to unlike posts.")
            response.status_code = 403
            return response

        post = db.get_post_by_id(strToInt(postID))
        if (not post):
            response = make_response("Post does not exist.")
            response.status_code = 404
            return response

        username = user["username"]
        if username not in post.get("liked_by", []):
            return jsonify({"error": "User has not liked this post"}), 400

        liked_by_updated = post.get("liked_by", [])
        liked_by_updated.remove(username)
        like_count = post["like_count"] - 1

        posts = db.init_mongo().posts
        posts.update_one({"post_id": strToInt(postID)}, {"$set": {"like_count": like_count, "liked_by": liked_by_updated}})

        return jsonify({"message": "Post unliked successfully", "likes": like_count + 1}), 200

    @app.after_request
    def set_nosniff(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        return response

    return app