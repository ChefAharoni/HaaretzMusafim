import datetime
import json

SITE_TXT = "site:"  # To access the site
BASE_URL = (
    "https://www.haaretz.co.il/magazine/"  # Starter of every musaf (magazine) url
)

# List of add-ons to the base url
add_ons = ["famous/", "ayelet-shani/"]

# Get today's date
TODAY = datetime.date.today()

# Calculate the start date (20 years ago)
start_date = TODAY - datetime.timedelta(days=365 * 20)

# Initialize an empty list to store the Friday dates
fridays = []

# Initialize an empty lize to store all the final links of the magazines (musafim)
magazines_urls = []
addon_urls = []  # Empty list for the addons
magazines = {}  # Empty dictionary for the dirs that will be created


def add_fridays():
    # Iterate over each date from the start date to today
    for date in (
        start_date + datetime.timedelta(n) for n in range((TODAY - start_date).days)
    ):
        # Check if the date is a Friday
        if date.weekday() == 4:  # 4 represents Friday (Monday is 0 and Sunday is 6)
            fridays.append(date)


def print_fridays():
    # Print the list of Friday dates
    print("Fridays:")
    for friday in fridays:
        print(friday)


def concat_dates():
    for friday in fridays:
        this_friday_articles = []
        this_friday_articles.append(
            "magazine/"
        )  # Perhaps change this to BASE_URL, depends on how final result will act.
        mag_url = SITE_TXT + BASE_URL + str(friday) + "/"
        magazines_urls.append(mag_url)
        for addon in add_ons:
            mag_url = SITE_TXT + BASE_URL + addon + str(friday) + "/"
            this_friday_articles.append(addon)
            addon_urls.append(mag_url)
        magazines[str(friday)] = this_friday_articles
    # print(magazines)
    # print(magazines_urls)


def merge_urls():
    # magazines
    with open("Fridays.json", "w") as file:
        json.dump(magazines, file, indent=4)


def main():
    add_fridays()
    concat_dates()
    merge_urls()


if __name__ == "__main__":
    main()
    print(len(fridays))  # Prints the length of the Fridays list
