from bs4 import BeautifulSoup
import requests
import json
from modules import group_dates


HAARETZ_SITEMAP = "https://www.haaretz.co.il/sitemap.xml"
# HAARETZ_SITEMAP = "https://www.haaretz.co.il/sitemap-202401.xml"


def fetch_sitemap():
    """
    Fetches the Haaretz sitemap and returns a list of URLs.
    """
    response = requests.get(HAARETZ_SITEMAP)
    soup = BeautifulSoup(response.content, "xml")
    sitemap = [loc.text for loc in soup.find_all("loc")]
    return sitemap


def save_sitemap_to_json():
    """
    Saves the Haaretz sitemap to a JSON file.
    """
    sitemap = fetch_sitemap()
    with open("data/haaretz_sitemap.json", "w") as file:
        json.dump(sitemap, file, indent=4)


def fetch_urls():
    """
    Fetches the Haaretz sitemap and returns a list of URLs.
    """
    # sitemap = open_sitemap_json()
    sitemap = fetch_sitemap()
    # mag_urls = open_mag_urls_json()
    mag_urls = open_json("data/haaretz_sitemap.json")
    for month in sitemap:
        if month in mag_urls.keys():
            print(f"Skipping: {month}")
            continue
        response = requests.get(month)
        print(f"Fetching URLs from: {month}")
        print(f"Response: {response}")
        soup = BeautifulSoup(response.content, "xml")
        urls = [loc.text for loc in soup.find_all("loc")]
        site_relevant_urls = []
        for url in urls:
            if url.startswith("https://www.haaretz.co.il/magazine/"):
                print(f"URL: {url}")
                site_relevant_urls.append(url)
        mag_urls[month] = site_relevant_urls
    # save_mag_urls_json(mag_urls)
    save_json("data/mag_urls.json", mag_urls)
    group_dates.main()
    return mag_urls


def add_titles():
    grouped_articles = open_json("data/grouped_articles.json")
    titled_urls = open_json("data/titled_urls.json")  # Load existing titled URLs

    for month, dates in grouped_articles.items():
        titled_urls[month] = {}
        for date, urls in dates.items():
            if month in titled_urls and date in titled_urls[month]:
                print(f"Skipping already processed date: {date} in {month}")
                continue

            # titled_urls[month][date] = {}
            # checks if a specified key exists in the dictionary. If the key is found, it returns the value associated with that key. If the key is not found, it adds the key with a default value.
            titled_urls.setdefault(month, {})[date] = {}
            print(f"Fetching titles for: {date}")
            for url in urls:
                title = get_title(url)
                titled_urls[month][date][url] = title if title else "No title found"
            print(f"Processed {date} for {month}")

        save_json("data/titled_urls.json", titled_urls)
    print("Titles added and saved.")


def get_title(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        title = soup.find("title").text
        print(f"Response: {response}")
        print(f"Title: {title}")
        print(f"URL: {url}")
    except Exception as e:
        print(f"Error fetching title for {url}: {e}")
        print(f"Response: {response}")
        title = None
    return title


def print_urls():
    urls = fetch_sitemap()
    for url in urls:
        print(url)


def fetch_months():
    urls = fetch_sitemap()
    articles = {}
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "xml")
        article = [loc.text for loc in soup.find_all("loc")]
        articles[url] = article
    return articles


# def open_sitemap_json():
#     with open("data/haaretz_sitemap.json", "r") as file:
#         sitemap = json.load(file)


# def open_mag_urls_json():
#     with open("data/mag_urls.json", "r") as file:
#         mag_urls = json.load(file)
#     return mag_urls


def open_json(fname):
    with open(fname, "r") as file:
        j_dict = json.load(file)
    return j_dict


def save_json(fname, dict):
    with open(fname, "w") as file:
        json.dump(dict, file, indent=4)


# def save_mag_urls_json(dict):
#     with open("data/mag_urls.json", "w") as file:
#         json.dump(dict, file, indent=4)


if __name__ == "__main__":
    # fetch_urls()
    add_titles()
