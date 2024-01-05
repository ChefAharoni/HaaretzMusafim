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
    """
    Display the links for a given date.

    Parameters:
    - date (str): The date for which to display the links.

    Returns:
    - str: The rendered HTML template with the links for the given date.
    """
    links = Fridays.get(
        date, []
    )  # Get the links for the given date, or an empty list if the date is not found.
    return render_template(
        "links.html", date=date, links=links
    )  # Render the template with the links.


if __name__ == "__main__":
    app.run(port=5000, debug=True)
