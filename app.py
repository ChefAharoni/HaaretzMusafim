from flask import Flask, request, render_template, url_for, jsonify, abort
from collections import defaultdict
import json
from datetime import datetime
from modules.old import fetchURL as fetch
from modules import dates_segments
import haaretz_scrape

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", segments=grouped_dates.keys())


@app.route("/segment/<int:segment>")
def show_segment(segment):
    print(
        f"Type of segment: {type(segment)}"
    )  # Used only to check the type of url, delete after hint is added
    dates = grouped_dates.get(segment, [])

    # Group dates by year
    years = defaultdict(list)
    for date in dates:
        year = date.split("-")[0]
        years[year].append(date)

    return render_template("segment.html", segment=segment, years=years)


@app.route("/date/<date>")
def show_links(date: str):
    titled_urls = haaretz_scrape.open_json("data/titled_urls.json")
    weekend_urls = {}
    print(f"Type: {type(date)}")
    for months in titled_urls:
        for dates in titled_urls[months]:
            if date in dates:
                print(f"Chosen date: {date}")
                weekend_urls = titled_urls[months][dates]
    print(f"Weekend URLs: {weekend_urls}")
    return render_template("links.html", date=date, weekend_urls=weekend_urls)


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
