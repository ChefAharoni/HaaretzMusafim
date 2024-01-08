import json
import re
from collections import defaultdict
from datetime import datetime, timedelta


def parse_date_from_url(url) -> datetime:
    """Extracts the date from the given URL."""
    print(
        f"Type of url: {type(url)}"
    )  # Used only to check the type of url, delete after hint is added
    match = re.search(r"\d{4}-\d{2}-\d{2}", url)
    if match:
        return datetime.strptime(match.group(), "%Y-%m-%d")
    return None


def get_weekend(date):
    """Returns the weekend date (Saturday) for the given date."""
    print(
        f"Type of date: {type(date)}"
    )  # Used only to check the type of url, delete after hint is added
    return date + timedelta(days=(5 - date.weekday()))


def group_articles_by_weekend(articles):
    print(
        f"Type of articles: {type(articles)}"
    )  # Used only to check the type of url, delete after hint is added
    grouped_articles = defaultdict(list)
    for article in articles:
        date = parse_date_from_url(article)
        if date:
            weekend = get_weekend(date)
            grouped_articles[weekend.strftime("%Y-%m-%d")].append(article)
    print(
        f"Type of grouped_articles: {type(grouped_articles)}"
    )  # Used only to check the type of url, delete after hint is added

    return grouped_articles


def main():
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


if __name__ == "__main__":
    main()
