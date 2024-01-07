from bs4 import BeautifulSoup
import requests


# HAARETZ_SITEMAP = "https://www.haaretz.co.il/sitemap.xml"
HAARETZ_SITEMAP = "https://www.haaretz.co.il/sitemap-202401.xml"


def fetch_sitemap():
    """
    Fetches the Haaretz sitemap and returns a list of URLs.
    """
    response = requests.get(HAARETZ_SITEMAP)
    soup = BeautifulSoup(response.content, "xml")
    urls = [loc.text for loc in soup.find_all("loc")]
    mag_urls = []
    for url in urls:
        if url.startswith("https://www.haaretz.co.il/magazine/"):
            mag_urls.append(url)
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


# print(fetch_sitemap())
# print(fetch_months())
print_urls()
