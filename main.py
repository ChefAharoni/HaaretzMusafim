import datetime

today = datetime.date.today()
print(f"Today's date is {today}")
print(f"Last week's date is {today - datetime.timedelta(days=7)}")
