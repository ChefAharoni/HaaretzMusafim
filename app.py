from flask import Flask, request, render_template, url_for, jsonify, abort
from collections import defaultdict
import json
from datetime import datetime
from modules.old import fetchURL as fetch
from modules import dates_segments
import subprocess
import hmac
import hashlib
import os

# from dotenv import load_dotenv
# from git import Repo


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", segments=grouped_dates.keys())


@app.route("/segment/<int:segment>")
def show_segment(segment):
    dates = grouped_dates.get(segment, [])

    # Group dates by year
    years = defaultdict(list)
    for date in dates:
        year = date.split("-")[0]
        years[year].append(date)

    return render_template("segment.html", segment=segment, years=years)


@app.route("/date/<date>")
def show_links(date):
    print(f"Date: {date}")


# def show_links_old(date):
#     # Check if the date is in the all_urls.json file
#     if fetch.check_date(date):
#         all_urls = fetch.open_json("all_urls.json")
#     # If the date is not in the all_urls.json file, fetch the URLs from Google
#     else:
#         google_links = Thursdays.get(date, [])
#         all_urls = fetch.open_json("all_urls.json")
#         print(f"Fetching for: {date}")
#         for google_link in google_links:
#             print(f"Fetching URLs from: {google_link}")  # Debugging print statement
#             fetch.fetch_actual_urls(google_link, date=date)

#         fetch.save_all_urls_json(date=date)
#         all_urls = fetch.open_json("all_urls.json")
#     return render_template("links.html", date=date, titles_urls=all_urls[date])


@app.context_processor
def inject_segments():
    """
    Injects segments into the response dictionary. This way, the grouped dates are available in every template.
    Returns:
        A dictionary containing the segments.
    """
    return {"segments": grouped_dates.keys()}


if __name__ == "__main__":
    grouped_dates = dates_segments.group_dates()
    app.run(port=5000, debug=True)
