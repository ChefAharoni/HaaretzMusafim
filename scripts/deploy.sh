#!/bin/bash

# Navigate to the project directory
cd /home/ec2-user/site/HaaretzMusafim || exit

# Activate the virtual environment
source haaretzENV/bin/activate

# Pull the latest changes
git reset --hard
git pull origin main  # Change "main" to your repo's default branch if different

# Install dependencies (if requirements.txt is updated)
pip install -r requirements.txt

# Restart Gunicorn and Nginx
sudo systemctl restart haaretz
sudo systemctl restart nginx

echo "Deployment successful at $(date)" >> /var/log/deploy.log
