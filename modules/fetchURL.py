import requests
from bs4 import BeautifulSoup
import urllib.parse


def fetch_actual_urls(google_search_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(google_search_url, headers=headers)
    print(f"Response Status: {response.status_code}")  # Check response status
    soup = BeautifulSoup(response.content, "html.parser")

    actual_urls = []
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        if "/url?q=" in href:
            # Extract and clean the URL
            clean_url = href.split("/url?q=")[1].split("&")[0]
            clean_url = urllib.parse.unquote(clean_url)
            print(clean_url)
            # Include only URLs that start with "haaretz"
            if clean_url.startswith("https://www.haaretz.co.il"):
                actual_urls.append(clean_url)

    return actual_urls
