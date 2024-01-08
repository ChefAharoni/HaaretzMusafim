import os
import sys

# Get the directory of your script
script_dir = os.path.dirname(__file__)

# Get the parent directory
parent_dir = os.path.dirname(script_dir)

# Add the parent directory to sys.path
sys.path.append(parent_dir)

# Now you can import the module in the parent directory
import haaretz_scrape

def test_open_links(date):
    grouped_articles = haaretz_scrape.open_json("data/grouped_articles.json")
    only_urls = []
    for url in grouped_articles:
        for weekend in grouped_articles[url]:
            if weekend == date:
                print(f"Date: {date}")
                print(f"URL: {grouped_articles[url][date]}")
                only_urls = grouped_articles[url][date]
                return only_urls

test_open_links("2020-01-04")
