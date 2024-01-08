import json
from datetime import datetime
from collections import defaultdict


def get_sitemap():
    with open("data/haaretz_sitemap.json", "r") as f:
        return json.load(f)


def get_dates():
    sitemap = get_sitemap()
    clean_dates = []
    for url in sitemap:
        if "latest" in url:
            continue
        date = url.split("-")[-1]
        date = date.split(".")[0]
        year = date[0:4]
        month = date[4:]
        clean_date = year + "-" + month
        clean_dates.append(clean_date)
    return clean_dates


def group_dates():
    # Group dates into five-year segments
    grouped = defaultdict(list)
    clean_dates = get_dates()
    for date in clean_dates:
        year = datetime.strptime(date, "%Y-%m").year
        segment = 5 * (year // 5)  # Grouping by every 5 years
        grouped[segment].append(date)

    # Sort dates within each segment
    for segment in grouped:
        grouped[segment].sort()

    return dict(grouped)


if __name__ == "__main__":
    # print(group_dates())
    group_dates()
