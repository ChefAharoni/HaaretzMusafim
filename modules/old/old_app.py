from flask import Flask, request, render_template, url_for, jsonify, abort
from collections import defaultdict
import json
from datetime import datetime
from modules.old import fetchURL as fetch
import subprocess
import hmac
import hashlib
import os

# from dotenv import load_dotenv
# from git import Repo


app = Flask(__name__)


with open("modules/old/Thursdays.json", "r") as f:
    Thursdays = json.load(f)


def group_dates(data):
    # Group dates into five-year segments
    grouped = defaultdict(list)
    for date in data:
        print(f"Date: {date}")
        print(f"Type of date: {type(date)}")
        year = datetime.strptime(date, "%Y-%m-%d").year
        segment = 5 * (year // 5)  # Grouping by every 5 years
        print(f"Segment: {segment}")
        grouped[segment].append(date)

    # Sort dates within each segment
    for segment in grouped:
        grouped[segment].sort()

    return dict(grouped)


grouped_dates = group_dates(Thursdays)
# print(grouped_dates)


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
    # Check if the date is in the all_urls.json file
    if fetch.check_date(date):
        all_urls = fetch.open_json("all_urls.json")
        # titles_urls = all_urls[date]  # Avoids calling all dates in html
    # If the date is not in the all_urls.json file, fetch the URLs from Google
    else:
        google_links = Thursdays.get(date, [])
        all_urls = fetch.open_json("all_urls.json")
        print(f"Fetching for: {date}")
        for google_link in google_links:
            print(f"Fetching URLs from: {google_link}")  # Debugging print statement
            # Fetches the URLs from Google, saves them to date_urls and to all_urls
            fetch.fetch_actual_urls(google_link, date=date)

        fetch.save_all_urls_json(date=date)
        all_urls = fetch.open_json("all_urls.json")
    return render_template("links.html", date=date, titles_urls=all_urls[date])


@app.context_processor
def inject_segments():
    """
    Injects segments into the response dictionary. This way, the grouped dates are available in every template.
    Returns:
        A dictionary containing the segments.
    """
    return {"segments": grouped_dates.keys()}


if __name__ == "__main__":
    app.run(port=5000, debug=True)
