import json
from datetime import datetime
from collections import defaultdict


def get_articles():
    with open("data/grouped_articles.json", "r") as f:
        return json.load(f)


def get_dates():
    articles = get_articles()
    l_weekends = []
    for months, weekends in articles.items():
        for weekend in weekends:
            l_weekends.append(weekend)
    return l_weekends


def group_dates():
    # Group dates into five-year segments
    grouped = defaultdict(list)
    clean_dates = get_dates()
    for date in clean_dates:
        year = datetime.strptime(date, "%Y-%m-%d").year
        segment = 5 * (year // 5)  # Grouping by every 5 years
        grouped[segment].append(date)

    # Sort dates within each segment
    for segment in grouped:
        grouped[segment].sort()

    return dict(grouped)


if __name__ == "__main__":
    print(group_dates())
    # group_dates()
    # get_dates()
