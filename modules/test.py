import json


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


# print(check_date("2023-12-28"))
# print(check_date("2023-12-20"))
