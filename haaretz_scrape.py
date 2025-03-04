from bs4 import BeautifulSoup
import requests
import json
from modules import group_dates
import logging
from modules.extensions import search_sort, update_algolia


HAARETZ_SITEMAP = "https://www.haaretz.co.il/sitemap.xml"


def open_json(fname: str) -> dict:
    """
    Opens a JSON file and returns its contents as a dictionary.

    Args:
        fname (str): The file name or path.

    Returns:
        dict: The contents of the JSON file as a dictionary.
    """
    with open(fname, "r") as file:
        j_dict = json.load(file)
        logging.info(f"Loaded {fname}")
    return j_dict


def save_json(fname: str, dict: dict) -> None:
    """
    Saves a dictionary as JSON to a file.

    Args:
        fname (str): The file name or path.
        dict (dict): The dictionary to be saved.

    Returns:
        None
    """
    with open(fname, "w") as file:
        json.dump(dict, file, indent=4)
        logging.info(f"Saved {fname}")


def fetch_sitemap():
    """
    Fetches the Haaretz sitemap and returns a list of URLs.

    Returns:
        list: A list of URLs from the Haaretz sitemap.
    """
    response = requests.get(HAARETZ_SITEMAP)  # Fetch the sitemap
    soup = BeautifulSoup(response.content, "xml")  # Parse the XML content
    sitemap = [
        loc.text for loc in soup.find_all("loc")
    ]  # Extract the URLs from the sitemap
    return sitemap


def save_sitemap_to_json():
    """
    Saves the Haaretz sitemap to a JSON file.

    Returns:
        None
    """
    sitemap = fetch_sitemap()
    with open("data/haaretz_sitemap.json", "w") as file:
        json.dump(sitemap, file, indent=4)


def fetch_urls():
    """
    Fetches the Haaretz sitemap and returns a list of URLs.

    Returns:
        dict: A dictionary containing the URLs grouped by month.
    """
    sitemap = fetch_sitemap()  # Fetch the sitemap
    mag_urls = open_json("data/mag_urls.json")  # Load existing URLs
    for month in sitemap:  # Iterate over the URLs in the sitemap
        if month in mag_urls.keys():  # Skip URLs that have already been processed
            print(f"Skipping: {month}")
            continue
        response = requests.get(month)
        print(f"Fetching URLs from: {month}")
        print(f"Response Code: {response.status_code}")
        soup = BeautifulSoup(response.content, "xml")
        urls = [loc.text for loc in soup.find_all("loc")]
        site_relevant_urls = []
        for url in urls:
            if url.startswith("https://www.haaretz.co.il/magazine/"):
                print(f"URL: {url}")
                site_relevant_urls.append(url)
        mag_urls[month] = site_relevant_urls
    save_json("data/mag_urls.json", mag_urls)
    group_dates.main()
    return mag_urls


def add_titles():
    """
    Fetches titles for articles and adds them to the 'titled_urls' dictionary.

    This function iterates over the 'grouped_articles' dictionary, which contains articles grouped by month and date.
    For each date, it fetches the titles for the corresponding URLs and adds them to the 'titled_urls' dictionary.
    The 'titled_urls' dictionary is then saved to a JSON file.

    Parameters:
    None

    Returns:
    None
    """
    grouped_articles = open_json("data/grouped_articles.json")
    titled_urls = open_json("data/titled_urls.json")  # Load existing titled URLs

    if titled_urls:
        print("Loaded existing titled URLs.")

    for month, dates in grouped_articles.items():
        for date, urls in dates.items():
            if month in titled_urls and date in titled_urls[month]:
                print(f"Skipping already processed date: {date} in {month}")
                continue

            titled_urls.setdefault(month, {})[date] = {}
            print(f"Fetching titles for: {date}")
            for url in urls:
                title = get_title(url)
                titled_urls[month][date][url] = title if title else "No title found"
            print(f"Processed {date} for {month}")

        save_json("data/titled_urls.json", titled_urls)
        print("Titles added and saved.")


def get_title(url: str) -> str:
    """
    Fetches the title of a web page given its URL.

    Args:
        url (str): The URL of the web page.

    Returns:
        str: The title of the web page, or None if an error occurred.
    """
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        title = soup.find("title").text
        print(f"Response: {response}")
        print(f"Title: {title}")
        print(f"URL: {url}")
    except Exception as e:
        response = requests.get(url)
        print(f"Error fetching title for {url}: {e}")
        print(f"Response: {response}")
        title = None
    return title


def fetch_months():
    """
    Fetches the articles grouped by month.

    Returns:
        dict: A dictionary containing the articles grouped by month.
    """
    urls = fetch_sitemap()
    articles = {}
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "xml")
        article = [loc.text for loc in soup.find_all("loc")]
        articles[url] = article
    return articles


def main():
    """
    Main function to fetch URLs, add titles, and perform search and sort operations.

    Returns:
        None
    """
    print("Fetching URLs...")
    fetch_urls()
    print("Adding titles...")
    add_titles()
    print("Organizing articles for search DB...")
    search_sort.main()
    print("Updating Algolia...")
    update_algolia.main()
    print("Algolia updated successfully.")


if __name__ == "__main__":
    main()
    add_titles()
