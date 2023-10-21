from flask import Flask, redirect, request, make_response, render_template

import os

import App.db as db

def create_app(test_config = None):
    app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb://mongo:27017/database"

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/")
    def index():
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

    @app.after_request
    def set_nosniff(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        return response
    
    return app