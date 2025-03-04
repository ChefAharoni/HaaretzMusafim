"""
Algolia integration module that updates the Algolia index with the latest data.

This module reads the algolia_compatible_data.json file and updates the Algolia index.
It's designed to be called after search_sort.py updates the algolia_compatible_data.json file.
"""

import json
import os
import hashlib
import logging
from algoliasearch.search_client import SearchClient
from algoliasearch.exceptions import AlgoliaException
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("update_algolia")

# Load environment variables
load_dotenv()

# Constants
ALGOLIA_APP_ID = "R0P8LNKXOK"
ALGOLIA_APP_KEY = os.getenv("ALGOLIA_APP_KEY")
ALGOLIA_INDEX_NAME = "HaaretzArchive Index"
BATCH_SIZE = 1000  # Number of records to send in each batch


def load_data():
    """
    Load data from the algolia_compatible_data.json file.

    Returns:
        list: List of dictionaries containing article data
    """
    try:
        with open("data/algolia_compatible_data.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            logger.info(f"Loaded {len(data)} records from algolia_compatible_data.json")
            return data
    except FileNotFoundError:
        logger.error("algolia_compatible_data.json file not found")
        return []
    except json.JSONDecodeError:
        logger.error("Error parsing algolia_compatible_data.json")
        return []


def add_object_ids(records):
    """
    Add unique objectID to each record based on URL.

    Args:
        records (list): List of record dictionaries

    Returns:
        list: Updated records with objectID
    """
    for record in records:
        if "url" in record:
            # Create a unique, consistent ID based on the URL
            record["objectID"] = hashlib.md5(record["url"].encode()).hexdigest()
        else:
            # Fallback to a combination of date and title if URL is missing
            id_string = f"{record.get('date', '')}-{record.get('title', '')}"
            record["objectID"] = hashlib.md5(id_string.encode()).hexdigest()

    return records


def batch_records(records, batch_size=BATCH_SIZE):
    """
    Split records into batches for efficient indexing.

    Args:
        records (list): List of record dictionaries
        batch_size (int): Size of each batch

    Returns:
        list: List of batches (lists of records)
    """
    return [records[i : i + batch_size] for i in range(0, len(records), batch_size)]


def update_algolia_index(clear_index=False):
    """
    Update the Algolia index with the latest data.

    Args:
        clear_index (bool): Whether to clear the index before adding new records

    Returns:
        bool: Success status
    """
    if not ALGOLIA_APP_KEY:
        logger.error("ALGOLIA_APP_KEY environment variable is not set")
        return False

    try:
        # Load and prepare data
        records = load_data()
        if not records:
            logger.warning("No records found to update")
            return False

        # Add objectIDs to records
        records = add_object_ids(records)

        # Connect to Algolia
        client = SearchClient.create(ALGOLIA_APP_ID, ALGOLIA_APP_KEY)
        index = client.init_index(ALGOLIA_INDEX_NAME)

        # Configure index settings
        index.set_settings(
            {
                "searchableAttributes": ["title", "date", "category"],
                "attributesForFaceting": ["date", "category"],
                "customRanking": ["desc(date)"],
                "attributesToHighlight": ["title"],
            }
        )

        # Clear the index if requested
        if clear_index:
            logger.info("Clearing index before update")
            index.clear_objects()

        # Split records into batches
        batches = batch_records(records)
        total_records = 0

        # Upload records in batches
        for i, batch in enumerate(batches):
            logger.info(f"Uploading batch {i+1}/{len(batches)} ({len(batch)} records)")
            result = index.save_objects(batch)
            result.wait()
            total_records += len(batch)

        logger.info(f"Successfully uploaded {total_records} records to Algolia")
        return True

    except AlgoliaException as e:
        logger.error(f"Algolia error: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return False


def main():
    """Main function to update the Algolia index."""
    logger.info("Starting Algolia index update")
    success = update_algolia_index()
    if success:
        logger.info("Algolia index update completed successfully")
    else:
        logger.error("Algolia index update failed")
    return success


if __name__ == "__main__":
    main()
