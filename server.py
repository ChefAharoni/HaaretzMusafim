from flask import Flask, request
import json

app = Flask(__name__)


@app.route("/{friday}", methods=["GET"])
def open_url():
    with open("Fridays.json", "r") as file:
        fridays = json.load(file)
