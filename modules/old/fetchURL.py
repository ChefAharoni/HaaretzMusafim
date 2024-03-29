import requests
from bs4 import BeautifulSoup
import urllib.parse
import json
import os
import datetime

# all_urls = {}  # Empty dictionary to store all URLs
date_urls = {}
PROXIES = {"http": "", "https": ""}


def fetch_actual_urls(google_search_url, date):
    """
    Fetches the actual URLs from a Google search page.

    Args:
        google_search_url (str): The URL of the Google search page.

    Returns:
        list: A list of actual URLs that start with "https://www.haaretz.co.il".
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(google_search_url, headers=headers, proxies=PROXIES)
    print(f"Response Status: {response.status_code}")  # Check response status
    soup = BeautifulSoup(response.content, "html.parser")
    dates = date_range(date)

    actual_urls = []
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        if "/url?q=" in href:
            # Extract and clean the URL
            clean_url = href.split("/url?q=")[1].split("&")[0]
            clean_url = urllib.parse.unquote(clean_url)
            # Include only URLs that start with "haaretz"
            if clean_url.startswith("https://www.haaretz.co.il"):
                # Include only URLs that contain the date
                if any(date in clean_url for date in dates):
                    actual_urls.append(clean_url)
                    if clean_url not in date_urls:
                        title = get_title(clean_url)
                        date_urls[clean_url] = title
                else:
                    print(f"URL does not contain {date}")
    # all_urls[date] = date_urls
    print(f"Date URLS: {date_urls}")
    return actual_urls


def date_range(date):
    """
    Returns a list of dates based on the given date.

    Args:
        date (str): The input date in the format "YYYY-MM-DD".

    Returns:
        list: A list containing the input date, the previous Wednesday, and the previous Tuesday.
    """
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    thursday = datetime.date(date.year, date.month, date.day)
    wed_date = str(thursday - datetime.timedelta(days=1))
    tue_date = str(thursday - datetime.timedelta(days=2))
    return [str(thursday), wed_date, tue_date]


def get_title(url):
    response = requests.get(url, proxies=PROXIES)
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

    reset_date_urls()


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


def reset_date_urls():
    global date_urls
    date_urls = {}  # Reset the dictionary
