import json


def extract_category(title):
    """
    Extracts the category from the title string.
    """
    parts = title.rsplit(" - ", 2)
    return parts[-2] if len(parts) >= 2 else "Unknown"


def transform_data(titled_urls):
    """
    Transforms the titled_urls dictionary into a list of dictionaries with keys 'date', 'title', 'url', 'category', and 'web_location'.
    """
    transformed_data = []

    for month, dates in titled_urls.items():
        for date, articles in dates.items():
            for url, title in articles.items():
                category = extract_category(title)
                web_location = f"/date/{date}"  # The web location path
                transformed_data.append(
                    {
                        "date": date,
                        "title": title,
                        "url": url,
                        "category": category,
                        "web_location": web_location,
                    }
                )

    return transformed_data


def main():
    """
    Loads the existing JSON data, transforms it, and saves the transformed data to a new JSON file.
    """
    with open("data/titled_urls.json", "r") as file:
        titled_urls = json.load(file)

    transformed_data = transform_data(titled_urls)

    # Print the length of the transformed data
    print(f"Length of transformed data: {len(transformed_data)}")

    with open("data/algolia_compatible_data.json", "w") as file:
        json.dump(transformed_data, file, indent=4)


if __name__ == "__main__":
    main()
