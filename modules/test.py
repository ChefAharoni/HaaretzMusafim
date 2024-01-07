import json
import fetchURL as fetch


def open_json(fname):
    # Opens a JSON file and returns a dictionary.
    with open(fname, "r") as file:
        return json.load(file)


all_urls = open_json("all_urls.json")


def print_all_urls():
    for date in all_urls:
        print(date)
        for url in all_urls[date]:
            print(url)
            print(all_urls[date][url])


def check_date(date):
    all_urls = open_json("all_urls.json")
    if date in all_urls.keys():
        return True
    else:
        return False


def show_links(date):
    # Check if the date is in the all_urls.json file
    if fetch.check_date(date):
        all_urls = fetch.open_json("all_urls.json")
        titles_urls = all_urls[date]
    return titles_urls


titles_urls = show_links("2023-12-28")
for url in titles_urls:
    print(f"URL: {url}")
    print(f"Title: {titles_urls[url]}")


# print(check_date("2023-12-28"))
# print(check_date("2023-12-20"))
