from flask import Flask, redirect, request, make_response, render_template, jsonify

import os

import App.db as db
import App.bcrypt as bcrypt

def strToInt(string: str):
    if (string is None):
        return None
    
    try:
        return int(string)
    except ValueError:
        return None

def create_app(test_config = None):
    app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb://mongo:27017/database"

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/")
    def index():
        user = db.get_user_by_request(request)
        if(user):
            return render_template("index.html", logged_username= user["username"])

        return render_template("index.html")

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

        return jsonify({"message": "Post liked successfully", "likes": like_count + 1}), 200

    @app.after_request
    def set_nosniff(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        return response
    
    return app