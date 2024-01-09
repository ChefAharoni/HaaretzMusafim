#!/bin/bash

# Activate the virtual environment
# source /path/to/your/venv/bin/activate
source workspace_env/bin/activate

# Install packages from requirements.txt
pip install -r /workspaces/HaaretzMusafim/requirements.txt
echo "Installing requirements..."
