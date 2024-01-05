from flask import Flask, request, render_template, url_for, jsonify
from collections import defaultdict
import json
from datetime import datetime


app = Flask(__name__)


with open("Thursdays.json", "r") as f:
    Thursdays = json.load(f)


def group_dates(data):
    # Group dates into five-year segments
    grouped = defaultdict(list)
    for date in data:
        year = datetime.strptime(date, "%Y-%m-%d").year
        segment = 5 * (year // 5)  # Grouping by every 5 years
        grouped[segment].append(date)
    return dict(grouped)


grouped_dates = group_dates(Thursdays)


@app.route("/")
def index():
    return render_template("index.html", segments=grouped_dates.keys())


@app.route("/segment/<int:segment>")
def show_segment(segment):
    dates = grouped_dates.get(segment, [])
    return render_template("segment.html", segment=segment, dates=dates)


@app.route("/date/<date>")
def show_links(date):
    """
    Display the links for a given date.

    Parameters:
    - date (str): The date for which to display the links.

    Returns:
    - str: The rendered HTML template with the links for the given date.
    """
    links = Thursdays.get(
        date, []
    )  # Get the links for the given date, or an empty list if the date is not found.
    return render_template(
        "links.html", date=date, links=links
    )  # Render the template with the links.


if __name__ == "__main__":
    app.run(port=5000, debug=True)
