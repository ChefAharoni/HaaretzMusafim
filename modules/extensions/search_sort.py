import json


def transform_data(titled_urls):
    """
    Transforms the given titled_urls dictionary into a list of dictionaries with keys 'date', 'title', and 'url'.

    Args:
        titled_urls (dict): A dictionary containing the titled URLs data.

    Returns:
        list: A list of dictionaries with transformed data.
    """
    transformed_data = []

    for month, dates in titled_urls.items():
        for date, articles in dates.items():
            for url, title in articles.items():
                transformed_data.append({"date": date, "title": title, "url": url})

    return transformed_data


def main():
    """
    Main function that loads the existing JSON data, transforms it, and saves the transformed data to a new JSON file.
    """
    # Load the existing JSON data
    with open("data/titled_urls.json", "r") as file:
        titled_urls = json.load(file)

    # Transform the data
    transformed_data = transform_data(titled_urls)

    # Save the transformed data to a new JSON file
    with open("data/algolia_compatible_data.json", "w") as file:
        json.dump(transformed_data, file, indent=4)


if __name__ == "__main__":
    main()
