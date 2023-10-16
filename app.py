from flask import Flask, request, make_response, render_template
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://mongo:27017/database"

mongo = PyMongo(app)

bcrypt = Bcrypt(app)

def hash(string):
    return bcrypt.generate_password_hash(string).decode('utf-8')

def hash_compare(hash, rawstring):
    return bcrypt.check_password_hash(hash, rawstring)


@app.route("/")
def index():
    return render_template("index.html")

@app.after_request
def set_nosniff(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response