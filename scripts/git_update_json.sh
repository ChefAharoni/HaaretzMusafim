#!/bin/bash
# This script updates the titled_urls.json to the repo every 5 minutes
# Repeat the process indefinitely
while true; do
    # Add all new or modified files to the staging area
    git add data/titled_urls.json

    # Commit the changes with a message
    git commit -m "Auto-Updated titled.urls.json"

    # Push the changes to the remote repository
    git push

    # Set the countdown time (5 minutes = 300 seconds)
    countdown=300

    # Countdown loop
    while [ $countdown -gt 0 ]; do
        echo "Time remaining before next run: $countdown seconds"
        sleep 10
        ((countdown-=10))
    done
done
