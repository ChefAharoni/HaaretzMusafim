from flask import Flask, request, render_template, url_for, jsonify, abort
from collections import defaultdict
import json
from datetime import datetime
from modules.old import fetchURL as fetch
from modules import dates_segments
import haaretz_scrape

app = Flask(__name__)

grouped_dates = dates_segments.group_dates()


@app.route("/")
def index():
    return render_template("index.html", segments=grouped_dates.keys())


@app.route("/segment/<int:segment>", defaults={"year": None})
@app.route("/segment/<int:segment>/<int:year>")
def show_segment(segment, year):
    dates = grouped_dates.get(segment, [])
    years = defaultdict(list)

    for date in dates:
        year_extracted = int(date.split("-")[0])
        years[year_extracted].append(date)

    if year is not None:
        # If a specific year is provided, filter dates to only include that year
        years = {year: years[year]}

    return render_template(
        "segment.html", segment=segment, years=years, scroll_to_year=year
    )


@app.route("/date/<date>")
def show_links(date: str):
    titled_urls = haaretz_scrape.open_json("data/titled_urls.json")  # With titles
    only_urls = open_links(date)
    weekend_urls = {}
    print(f"Type: {type(date)}")
    for months in titled_urls:
        for dates in titled_urls[months]:
            if date in dates:
                print(f"Chosen date: {date}")
                weekend_urls = titled_urls[months][dates]
    print(f"Weekend URLs: {weekend_urls}")
    return render_template(
        "links.html", date=date, weekend_urls=weekend_urls, only_urls=only_urls
    )


def open_links(date: str) -> list:
    grouped_articles = haaretz_scrape.open_json("data/grouped_articles.json")
    only_urls = []
    for url in grouped_articles:
        for weekend in grouped_articles[url]:
            if weekend == date:
                only_urls = grouped_articles[url][date]
                return only_urls


@app.context_processor
def inject_segments():
    """
    Injects segments and segment years into the response dictionary.
    This way, the grouped dates and years are available in every template.
    Returns:
        A dictionary containing the segments and segment years.
    """
    segment_years = defaultdict(list)
    for segment, dates in grouped_dates.items():
        for date in dates:
            year = date.split("-")[0]
            segment_years[segment].append(year)
        segment_years[segment] = sorted(list(set(segment_years[segment])))

    return {"segments": grouped_dates.keys(), "segment_years": segment_years}

@app.route("/ads")
def support_us():
    return render_template("ads.html")


@app.route("/privacy_policy")
def privacy_policy():
    return render_template("privacy_policy.html")


if __name__ == "__main__":
    app.run(port=5000, debug=True)
