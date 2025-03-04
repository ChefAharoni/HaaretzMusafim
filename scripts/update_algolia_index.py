#!/usr/bin/env python3
"""
Standalone script to update the Algolia index with data from the JSON file.
This can be run separately from the main scraping process.

Usage:
    python update_algolia_index.py
"""

import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from modules.extensions import update_algolia

if __name__ == "__main__":
    print("Starting Algolia index update...")
    update_algolia.main()
    print("Done.")
