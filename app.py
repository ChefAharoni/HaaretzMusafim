from flask import Flask, request, render_template, url_for, jsonify, abort
from collections import defaultdict
import json
from datetime import datetime
from modules import fetchURL as fetch
import subprocess
import hmac
import hashlib
import os
from dotenv import load_dotenv
from git import Repo


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

    # Sort dates within each segment
    for segment in grouped:
        grouped[segment].sort()

    return dict(grouped)


grouped_dates = group_dates(Thursdays)


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
    # If the date is not in the all_urls.json file, fetch the URLs from Google
    else:
        google_links = Thursdays.get(date, [])
        actual_links = []
        all_urls = fetch.open_json("all_urls.json")
        for google_link in google_links:
            print(f"Fetching URLs from: {google_link}")  # Debugging print statement
            fetched_urls = fetch.fetch_actual_urls(google_link)
            # actual_links.extend(fetched_urls)

        fetch.save_all_urls_json(date=date)
        all_urls = fetch.open_json("all_urls.json")
    return render_template("links.html", date=date, all_urls=all_urls)


@app.context_processor
def inject_segments():
    """
    Injects segments into the response dictionary. This way, the grouped dates are available in every template.
    Returns:
        A dictionary containing the segments.
    """
    return {"segments": grouped_dates.keys()}


# @app.route('/update_server', methods=['POST'])
#     def webhook():
#         if request.method == 'POST':
#             repo = git.Repo('path/to/git_repo')
#             origin = repo.remotes.origin
# origin.pull()
# return 'Updated PythonAnywhere successfully', 200
#         else:
#             return 'Wrong event type', 400

load_dotenv()  # This loads the .env file

# Access your variable
# GITHUB_SECRET = os.getenv("GITHUB_SECRET")
GITHUB_WEBHOOK_ROUTE = "/server_update"
GITHUB_SECRET = bytes(os.getenv("GITHUB_SECRET"), "utf-8")


@app.route(GITHUB_WEBHOOK_ROUTE, methods=["POST"])
def github_webhook():
    # Verify the request signature
    signature = request.headers.get("X-Hub-Signature")
    if signature is None:
        abort(403)

    sha_name, signature = signature.split("=")
    if sha_name != "sha1":
        abort(501)

    mac = hmac.new(GITHUB_SECRET, msg=request.data, digestmod=hashlib.sha1)
    if not hmac.compare_digest(mac.hexdigest(), signature):
        abort(403)

    # If the signature is valid, pull the latest changes
    subprocess.call(["git", "pull"])
    if request.method == "POST":
        repo = Repo("https://github.com/ChefAharoni/HaaretzMusafim")
        origin = repo.remotes.origin
        origin.pull()
        # Restart the server (this is a placeholder, replace with your server's restart command)
        os.system("restart server_command")
        return "Updated and restarted PythonAnywhere successfully", 200
    # Add any other commands you need to run after pulling changes, such as restarting your server
    # subprocess.call(['touch', '/var/www/html/myapp.wsgi'])

    return "Updated PythonAnywhere successfully", 200


if __name__ == "__main__":
    app.run(port=5000, debug=True)
