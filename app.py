from flask import Flask, request, render_template, url_for
import json

app = Flask(__name__)


@app.route("/{friday}", methods=["GET"])
def open_url():
    with open("Fridays.json", "r") as file:
        fridays = json.load(file)


@app.route("/")
def hello_world():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(port=5000, debug=True)
