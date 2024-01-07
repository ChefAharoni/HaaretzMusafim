import json
import modules.old.fetchURL as fetch
import datetime


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


def print_title_url(date):
    titles_urls = show_links(date)
    for url in titles_urls:
        print(f"URL: {url}")
        print(f"Title: {titles_urls[url]}")


def date_range(date):
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    thursday = datetime.date(date.year, date.month, date.day)
    wed_date = str(thursday - datetime.timedelta(days=1))
    tue_date = str(thursday - datetime.timedelta(days=2))
    return [str(thursday), wed_date, tue_date]


def add_thursdays():
    TODAY = datetime.date.today()
    start_date = TODAY - datetime.timedelta(days=365 * 2)
    thursdays = []

    # Iterate over each date from the start date to today
    for date in (
        start_date + datetime.timedelta(n) for n in range((TODAY - start_date).days)
    ):
        # Check if the date is a thursday
        if date.weekday() == 3:  # 3 represents Thursday (Monday is 0 and Sunday is 6)
            thursdays.append(date)
    return thursdays


# print(add_thursdays())
print(date_range("2024-01-04"))

# print(check_date("2023-12-28"))
# print(check_date("2023-12-20"))
