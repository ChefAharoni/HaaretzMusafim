import json
import hashlib
from datetime import datetime


def extract_category(title):
    """
    Extracts the category from the title string.
    """
    parts = title.rsplit(" - ", 2)
    return parts[-2] if len(parts) >= 2 else "Unknown"


def transform_data(titled_urls):
    """
    Transforms the titled_urls dictionary into a list of dictionaries with keys:
    'objectID', 'date', 'title', 'url', 'category', 'web_location', 'timestamp', and 'month'.
    """
    transformed_data = []

    for month, dates in titled_urls.items():
        for date, articles in dates.items():
            try:
                # Convert date to timestamp for sorting
                date_obj = datetime.strptime(date, "%Y-%m-%d")
                timestamp = int(date_obj.timestamp())
                year = date_obj.year
                month_num = date_obj.month
            except ValueError:
                # If date parsing fails, use default values
                timestamp = 0
                year = 0
                month_num = 0

            for url, title in articles.items():
                category = extract_category(title)
                web_location = f"/date/{date}"  # The web location path

                # Generate a unique objectID based on URL
                object_id = hashlib.md5(url.encode("utf-8")).hexdigest()

                transformed_data.append(
                    {
                        "objectID": object_id,
                        "date": date,
                        "year": year,
                        "month": month_num,
                        "timestamp": timestamp,  # For sorting by date
                        "title": title,
                        "url": url,
                        "category": category,
                        "web_location": web_location,
                        "source_month": month,  # Keep track of source month
                    }
                )

    return transformed_data


def main():
    """
    Loads the existing JSON data, transforms it, and saves the transformed data to a new JSON file.
    """
    try:
        with open("data/titled_urls.json", "r", encoding="utf-8") as file:
            titled_urls = json.load(file)

        transformed_data = transform_data(titled_urls)

        # Print the length of the transformed data
        print(f"Length of transformed data: {len(transformed_data)}")

        with open("data/algolia_compatible_data.json", "w", encoding="utf-8") as file:
            json.dump(transformed_data, file, indent=4, ensure_ascii=False)

        print("Successfully created Algolia-compatible data file")
        return True
    except Exception as e:
        print(f"Error creating Algolia-compatible data: {e}")
        return False


if __name__ == "__main__":
    main()
