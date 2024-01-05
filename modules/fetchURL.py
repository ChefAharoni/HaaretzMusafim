import requests
from bs4 import BeautifulSoup
import urllib.parse

# List of domains to exclude
excluded_domains = [
    "https://accounts.google",
    "https://maps.google",
    "https://support.google",
]


def fetch_actual_urls(google_search_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(google_search_url, headers=headers)

    soup = BeautifulSoup(response.content, "html.parser")

    actual_urls = []
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        if "/url?q=" in href:
            # Extract and clean the URL
            clean_url = href.split("/url?q=")[1].split("&")[0]
            clean_url = urllib.parse.unquote(clean_url)

            # Filter out URLs from excluded domains
            if not any(domain in clean_url for domain in excluded_domains):
                actual_urls.append(clean_url)

    return actual_urls
