"""Merged per-date link lookup used by the static build.

A weekend date can appear under two month sitemaps. The live Flask view shows
only one month's half; this merges every month's links for the date.
"""
import json


def _load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_date_links(titled_path="data/titled_urls.json",
                    grouped_path="data/grouped_articles.json"):
    """Return {date: (titled {url: title}, bare [urls])} across all months."""
    titled = _load(titled_path)
    grouped = _load(grouped_path)
    result = {}
    for _month, weekends in grouped.items():
        for date, urls in weekends.items():
            entry = result.setdefault(date, ({}, []))
            for u in urls:
                if u not in entry[1]:
                    entry[1].append(u)
    for _month, weekends in titled.items():
        for date, url_titles in weekends.items():
            if date in result:
                result[date][0].update(url_titles)
    return result
