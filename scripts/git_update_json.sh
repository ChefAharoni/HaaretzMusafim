#!/bin/bash
# This script updates the titled_urls.json to the repo every 5 minutes
# Repeat the process indefinitely
while true; do
    # Add all new or modified files to the staging area
    git add .

    # Commit the changes with a message
    git commit -m "update"

    # Push the changes to the remote repository
    git push

    # Wait for 5 minutes (300 seconds)
    sleep 300
done
