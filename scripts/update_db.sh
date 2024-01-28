#!/bin/bash
git pull
if [ $? -ne 0 ]; then
    echo "Git pull failed, exiting..."
    exit 1
fi

python haaretz_scrape.py
if [ $? -ne 0 ]; then
    echo "Python script failed, exiting..."
    exit 1
fi

git add data/*  # Add all JSON files from the data dir.
DATE=$(date)
git commit -m "Auto updated magazines URLs via Script on $DATE"
if [ $? -ne 0 ]; then
    echo "Git commit failed, exiting..."
    exit 1
fi

git push
if [ $? -ne 0 ]; then
    echo "Git push failed, exiting..."
    exit 1
fi
