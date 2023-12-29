#!/usr/bin/env bash

# Set up and activate the Python3 virtual environment.
python3 -m venv .venv
source .venv/bin/activate

# Install required Python modules.
pip install -Ur requirements.txt
