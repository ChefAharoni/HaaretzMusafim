import datetime
import datetime

# Get today's date
today = datetime.date.today()

# Calculate the start date (20 years ago)
start_date = today - datetime.timedelta(days=365 * 20)

# Initialize an empty list to store the Friday dates
fridays = []

# Iterate over each date from the start date to today
for date in (
    start_date + datetime.timedelta(n) for n in range((today - start_date).days)
):
    # Check if the date is a Friday
    if date.weekday() == 4:  # 4 represents Friday (Monday is 0 and Sunday is 6)
        fridays.append(date)


# Print the list of Friday dates
def print_fridays():
    print("Fridays:")
    for friday in fridays:
        print(friday)


print(len(fridays))
