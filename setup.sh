#!/bin/bash

# Exit script on any error
set -e

# Log file
mkdir -p ./logging
LOGFILE="./logging/setup_env.log"

# Create virtual environment
echo "Creating virtual environment '.venv'..." | tee -a $LOGFILE
python3 -m venv .venv

# Activate virtual environment
echo "Activating virtual environment..." | tee -a $LOGFILE
source .venv/bin/activate

# Install requirements
echo "Installing dependencies from requirements.txt..." | tee -a $LOGFILE
pip install -r requirements.txt

# Log completion
echo "Setup completed successfully on $(date)" | tee -a $LOGFILE
