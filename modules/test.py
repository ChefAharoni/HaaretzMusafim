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


def get_weekends(articles):
    weekends = defaultdict(list)
    for article in articles:
        date = parse_date_from_url(article)
        print(f"Date: {date}")
        if date:
            weekend = get_weekend(date)
            weekend = weekend.strftime("%Y-%m-%d")
    print(f"Weekends: {weekends}")
    return weekends


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


def main():
    # Load your existing JSON
    with open("data/mag_urls.json", "r") as file:
        data = json.load(file)

    # Process each month
    for month, articles in data.items():
        # print(f"Month: {month}")
        grouped_articles = get_weekend(articles)
        # data[month] = grouped_articles
        # print(data[month])
        # print(f"Month: {month}")

    # Save the new JSON structure
    with open("data/date_segments.json", "w") as file:
        json.dump(data, file, indent=4)


if __name__ == "__main__":
    main()
