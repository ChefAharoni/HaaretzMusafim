from bs4 import BeautifulSoup
import requests
import json


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
    with open("haaretz_sitemap.json", "w") as file:
        json.dump(sitemap, file, indent=4)


def fetch_urls():
    """
    Fetches the Haaretz sitemap and returns a list of URLs.
    """
    # sitemap = open_sitemap_json()
    sitemap = fetch_sitemap()
    mag_urls = open_mag_urls_json()
    for month in sitemap:
        response = requests.get(month)
        print(f"Fetching URLs from: {month}")
        print(f"Response: {response}")
        soup = BeautifulSoup(response.content, "xml")
        urls = [loc.text for loc in soup.find_all("loc")]
        site_relevant_urls = []
        for url in urls:
            # print(f"URL: {url}")
            if url.startswith("https://www.haaretz.co.il/magazine/"):
                print(f"URL: {url}")
                site_relevant_urls.append(url)
        mag_urls[month] = site_relevant_urls
        save_mag_urls_json(mag_urls)
    return mag_urls


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


def open_sitemap_json():
    with open("haaretz_sitemap.json", "r") as file:
        sitemap = json.load(file)
    # print(sitemap)


def open_mag_urls_json():
    with open("mag_urls.json", "r") as file:
        mag_urls = json.load(file)
    return mag_urls


def save_mag_urls_json(dict):
    with open("mag_urls.json", "w") as file:
        json.dump(dict, file, indent=4)


# print(fetch_months())
# print_urls()
# print_sitemap()
if __name__ == "__main__":
    fetch_urls()
    # sitemap = fetch_sitemap()
    # for l in sitemap:
    #     print(l)
