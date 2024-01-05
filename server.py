from flask import Flask, request
import json

app = Flask(__name__)


@app.route("/{friday}", methods=["GET"])
