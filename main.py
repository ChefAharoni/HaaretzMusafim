import datetime

SITE_TXT = "site:"  # To access the site
BASE_URL = (
    "https://www.haaretz.co.il/magazine/"  # Starter of every musaf (magazine) url
)

add_ons = ["famous/", "ayelet-shani/"]

# Get today's date
TODAY = datetime.date.today()

# Calculate the start date (20 years ago)
start_date = TODAY - datetime.timedelta(days=365 * 20)

# Initialize an empty list to store the Friday dates
fridays = []

# Initialize an empty lize to store all the final links of the magazines (musafim)
magazines_urls = []


def add_fridays():
    # Iterate over each date from the start date to today
    for date in (
        start_date + datetime.timedelta(n) for n in range((TODAY - start_date).days)
    ):
        # Check if the date is a Friday
        if date.weekday() == 4:  # 4 represents Friday (Monday is 0 and Sunday is 6)
            fridays.append(date)


# Print the list of Friday dates
def print_fridays():
    print("Fridays:")
    for friday in fridays:
        print(friday)


def concat_dates():
    for friday in fridays:
        mag_url = SITE_TXT + BASE_URL + str(friday) + "/"
        magazines_urls.append(mag_url)
    print(magazines_urls)


def main():
    add_fridays()
    concat_dates()


if __name__ == "__main__":
    main()
    print(len(fridays))  # Prints the length of the Fridays list
