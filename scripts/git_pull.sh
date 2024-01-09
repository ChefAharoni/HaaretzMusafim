#!/bin/bash
# This script auto-pulls the repo every 10 minutes
# Repeat the process indefinitely
while true; do
    # Push the changes to the remote repository
    git pull

    # Set the countdown time (10 minutes = 600 seconds)
    countdown=600

    # Countdown loop
    while [ $countdown -gt 0 ]; do
        echo "Time remaining before next run: $countdown seconds"
        sleep 10
        ((countdown-=10))
    done
done
