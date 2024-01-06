import datetime
import json


GOOGLE_SEARCH_URL = "https://www.google.com/search?q="
SITE_TXT = "site:"  # To access the site
BASE_URL = (
    "https://www.haaretz.co.il/magazine/"  # Starter of every musaf (magazine) url
)

# List of add-ons to the base url
add_ons = ["famous/", "ayelet-shani/", "20questions/", "ratingcommittee/", "blacklist/"]

# Get today's date
TODAY = datetime.date.today()

# Calculate the start date (20 years ago)
start_date = TODAY - datetime.timedelta(days=365 * 20)

# Initialize an empty list to store the thursday dates
thursdays = []

# Empty dictionary for the magazines; key is the date and value is a list of URLs
magazines = {}


def add_thursdays():
    # Iterate over each date from the start date to today
    for date in (
        start_date + datetime.timedelta(n) for n in range((TODAY - start_date).days)
    ):
        # Check if the date is a thursday
        if date.weekday() == 3:  # 3 represents Thursday (Monday is 0 and Sunday is 6)
            thursdays.append(date)


def concat_dates():
    url_prefix = GOOGLE_SEARCH_URL + SITE_TXT + BASE_URL
    for thursday in thursdays:
        wed_suffix = str(thursday - datetime.timedelta(days=1)) + "/"
        this_thursday_articles = (
            []
        )  # Saving as a list so values can be appended and added to each key of a thursday
        mag_url = url_prefix + str(thursday) + "/"
        wed_mag_url = url_prefix + str(thursday - datetime.timedelta(days=1)) + "/"
        tue_mag_url = url_prefix + str(thursday - datetime.timedelta(days=2)) + "/"
        wed_underthesun_mag_url = url_prefix + "underthesun/" + wed_suffix
        quote_mag_url = url_prefix + "quote/" + wed_suffix
        the_edge_mag_url = url_prefix + "the-edge/" + wed_suffix

        this_thursday_articles.append(mag_url)
        this_thursday_articles.append(wed_mag_url)
        this_thursday_articles.append(tue_mag_url)
        this_thursday_articles.append(wed_underthesun_mag_url)
        this_thursday_articles.append(quote_mag_url)
        this_thursday_articles.append(the_edge_mag_url)
        for addon in add_ons:
            mag_url = url_prefix + addon + str(thursday) + "/"
            this_thursday_articles.append(mag_url)
        magazines[str(thursday)] = this_thursday_articles


def merge_urls():
    # Saves the magazines dictionary into a JSON file called "thursdays.json".
    with open("Thursdays.json", "w") as file:
        json.dump(magazines, file, indent=4)


def main():
    add_thursdays()
    concat_dates()
    merge_urls()


if __name__ == "__main__":
    main()
    print(len(thursdays))  # Prints the length of the thursdays list
