from flask import Flask, request, make_response, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.after_request
def set_nosniff(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response