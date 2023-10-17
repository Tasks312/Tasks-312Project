from flask import Flask, request, make_response, render_template

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
    def register(response):
        username = request.form["username"]
        password = request.form["password"]

        token, err = db.register(username, password)

        if (err):
            response = make_response(err)
            response.status_code = 400
            return response

        response = make_response("OK")
        response.status_code = 200
        response.set_cookie("authtoken", token, max_age=36000, httponly = True)
        return response


    @app.after_request
    def set_nosniff(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        return response
    
    return app