# hello_algolia.py
from algoliasearch.search_client import SearchClient
import os
import json

# Load environment variables from .env file

# ALGOLIA_APP_KEY = os.environ["ALGOLIA_APP_KEY"]
ALGOLIA_APP_KEY = os.getenv("ALGOLIA_APP_KEY")


def open_json(fname: str) -> dict:
    with open(fname, "r") as file:
        j_dict = json.load(file)
    return j_dict


def hello_algolia():
    """
    A simple function to demonstrate Algolia integration.
    """
    # Connect and authenticate with your Algolia app
    client = SearchClient.create("R0P8LNKXOK", ALGOLIA_APP_KEY)

    # Create a new index and add a record
    index = client.init_index("HaaretzArchive Index")
    # record = {"objectID": 1, "name": "test_record"}
    titled_urls = open_json("data/titled_urls.json")
    index.save_object(titled_urls).wait()

    # Search the index and print the results
    results = index.search("2012-06-30")
    print(results["hits"][0])


hello_algolia()
