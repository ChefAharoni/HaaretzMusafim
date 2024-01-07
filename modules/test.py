import json


def open_json(fname):
    # Opens a JSON file and returns a dictionary.
    with open(fname, "r") as file:
        return json.load(file)


all_urls = open_json("all_urls.json")

for date in all_urls:
    print(date)
    for url in all_urls[date]:
        print(url)
        print(all_urls[date][url])
