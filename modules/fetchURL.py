import requests
from bs4 import BeautifulSoup
import urllib.parse
import json
import os

# all_urls = {}  # Empty dictionary to store all URLs
date_urls = {}


def fetch_actual_urls(google_search_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(
        google_search_url, headers=headers, proxies={"http": "", "https": ""}
    )
    print(f"Response Status: {response.status_code}")  # Check response status
    soup = BeautifulSoup(response.content, "html.parser")

    actual_urls = []
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        if "/url?q=" in href:
            # Extract and clean the URL
            clean_url = href.split("/url?q=")[1].split("&")[0]
            clean_url = urllib.parse.unquote(clean_url)
            # print(clean_url)
            # Include only URLs that start with "haaretz"
            if clean_url.startswith("https://www.haaretz.co.il"):
                actual_urls.append(clean_url)
                if clean_url not in date_urls:
                    title = get_title(clean_url)
                    date_urls[clean_url] = title
    # all_urls[date] = date_urls
    return actual_urls


def get_title(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.find("title").text
    print(f"Title: {title}")
    print(f"URL: {url}")
    return title


def save_all_urls_json(date, dict=date_urls, fname="all_urls.json"):
    # Saves a dictionary into a JSON file.
    all_urls = open_json(fname=fname)
    all_urls[date] = dict

    with open(fname, "w") as file:
        json.dump(all_urls, file, indent=4)


def open_json(fname):
    # Opens a JSON file and returns a dictionary.
    with open(fname, "r") as file:
        return json.load(file)


def check_date(date):
    all_urls = open_json("all_urls.json")
    if date in all_urls.keys() and all_urls[date] != {}:
        return True
    else:
        return False
