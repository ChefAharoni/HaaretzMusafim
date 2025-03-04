import json
import os
import hashlib
import logging
from typing import List, Dict, Any, Optional

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("algolia_updater")

# Global flag to track if algoliasearch is available
ALGOLIA_AVAILABLE = False

# Try to import algoliasearch, but don't fail if it's not available
try:
    from algoliasearch.search_client import SearchClient

    ALGOLIA_AVAILABLE = True
except ImportError:
    logger.warning(
        "algoliasearch package not installed. Algolia updates will be skipped."
    )
    logger.warning("To enable Algolia updates, run: pip install algoliasearch")


def load_json_data(file_path: str) -> List[Dict[str, Any]]:
    """
    Load and return data from a JSON file

    Args:
        file_path: Path to the JSON file

    Returns:
        List of records from the JSON file
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        logger.info(f"Successfully loaded data from {file_path}")
        return data
    except Exception as e:
        logger.error(f"Error loading data from {file_path}: {e}")
        return []


def prepare_records(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Prepare records for Algolia indexing by adding objectID

    Args:
        data: List of data records

    Returns:
        Records prepared for Algolia indexing
    """
    try:
        for record in data:
            # Generate a unique objectID using URL to ensure idempotence
            if "url" in record and not "objectID" in record:
                record["objectID"] = hashlib.md5(
                    record["url"].encode("utf-8")
                ).hexdigest()

            # Ensure all text fields are strings
            for key, value in record.items():
                if isinstance(value, (list, dict)):
                    record[key] = json.dumps(value)

        logger.info(f"Prepared {len(data)} records for indexing")
        return data
    except Exception as e:
        logger.error(f"Error preparing records: {e}")
        return []


ALGOLIA_APP_ID = os.getenv("ALGOLIA_APP_ID")


def update_algolia_index(
    app_id: str = ALGOLIA_APP_ID,
    index_name: str = "HaaretzArchive Index",
    data_file: str = "data/algolia_compatible_data.json",
    batch_size: int = 1000,
) -> bool:
    """
    Update the Algolia index with data from the specified file

    Args:
        app_id: Algolia application ID
        index_name: Name of the Algolia index
        data_file: Path to the data file
        batch_size: Size of batches for indexing

    Returns:
        True if successful, False otherwise
    """
    # Check if algoliasearch is available
    if not ALGOLIA_AVAILABLE:
        logger.error("Cannot update Algolia index: algoliasearch package not installed")
        logger.error("Please run: pip install algoliasearch")
        return False

    # Get Algolia admin key from environment variables
    admin_key = os.getenv("ALGOLIA_APP_KEY")

    if not admin_key:
        logger.error("ALGOLIA_APP_KEY environment variable not found")
        return False

    try:
        # Load data from file
        data = load_json_data(data_file)
        if not data:
            logger.error("No data to index")
            return False

        # Prepare records for indexing
        records = prepare_records(data)
        if not records:
            logger.error("Failed to prepare records")
            return False

        # Initialize Algolia client
        logger.info(f"Connecting to Algolia with app ID: {app_id}")
        client = SearchClient.create(app_id, admin_key)
        index = client.init_index(index_name)

        # Configure index settings
        index.set_settings(
            {
                "searchableAttributes": ["title", "date", "category"],
                "attributesForFaceting": ["category", "date"],
                "customRanking": ["desc(date)"],
            }
        )

        # Index records in batches
        total_records = len(records)
        for i in range(0, total_records, batch_size):
            batch = records[i : i + batch_size]
            index.save_objects(batch).wait()
            logger.info(
                f"Indexed batch {i//batch_size + 1}/{(total_records+batch_size-1)//batch_size} ({len(batch)} records)"
            )

        logger.info(f"Successfully indexed {total_records} records to Algolia")
        return True

    except Exception as e:
        logger.error(f"Error updating Algolia index: {e}")
        return False


def main():
    """
    Main function to update Algolia index
    """
    if not ALGOLIA_AVAILABLE:
        logger.warning("Skipping Algolia update: algoliasearch package not installed")
        return False

    success = update_algolia_index()
    if success:
        logger.info("Algolia index update completed successfully")
    else:
        logger.error("Algolia index update failed")

    return success


if __name__ == "__main__":
    main()
