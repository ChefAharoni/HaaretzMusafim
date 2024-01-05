from flask import Flask, request, render_template, url_for, jsonify
import json

app = Flask(__name__)


with open("Fridays.json", "r") as f:
    Fridays = json.load(f)


@app.route("/")
def index():
    return render_template("index.html", dates=Fridays.keys())


@app.route("/date/<date>")
def show_links(date):
    links = Fridays.get(date, [])
    return render_template("links.html", date=date, links=links)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
