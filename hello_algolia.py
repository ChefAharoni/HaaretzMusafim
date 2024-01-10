# hello_algolia.py
from algoliasearch.search_client import SearchClient
import os

# ALGOLIA_APP_KEY = os.environ["ALGOLIA_APP_KEY"]
ALGOLIA_APP_KEY = os.getenv('ALGOLIA_APP_KEY')

# Connect and authenticate with your Algolia app
client = SearchClient.create("R0P8LNKXOK", ALGOLIA_APP_KEY)

# Create a new index and add a record
index = client.init_index("HaaretzArchive Index")
record = {"objectID": 1, "name": "test_record"}
index.save_object(record).wait()

# Search the index and print the results
results = index.search("test_record")
print(results["hits"][0])
