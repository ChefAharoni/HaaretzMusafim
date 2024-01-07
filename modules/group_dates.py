import json
import re
from collections import defaultdict
from datetime import datetime, timedelta


def parse_date_from_url(url):
    """Extracts the date from the given URL."""
    match = re.search(r"\d{4}-\d{2}-\d{2}", url)
    if match:
        return datetime.strptime(match.group(), "%Y-%m-%d")
    return None


def get_weekend(date):
    """Returns the weekend date (Saturday) for the given date."""
    return date + timedelta(days=(5 - date.weekday()))


def group_articles_by_weekend(articles):
    grouped_articles = defaultdict(list)
    for article in articles:
        date = parse_date_from_url(article)
        if date:
            weekend = get_weekend(date)
            grouped_articles[weekend.strftime("%Y-%m-%d")].append(article)
    return grouped_articles


# Load your existing JSON
with open("data/mag_urls.json", "r") as file:
    data = json.load(file)

# Process each month
for month, articles in data.items():
    grouped_articles = group_articles_by_weekend(articles)
    data[month] = grouped_articles

# Save the new JSON structure
with open("data/grouped_articles.json", "w") as file:
    json.dump(data, file, indent=4)
