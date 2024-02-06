#!/bin/bash

# Check if the script is run as root
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root. Please use sudo or run as root."
    exit 1
fi

# Get the parent directory of the current directory
parent_directory="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && cd .. && pwd )"

# Define the log file path
log_file="$parent_directory/main.log"

# Check if main.py exists in the parent directory
if [ -e "$parent_directory/main.py" ]; then
    # Redirect the output and errors of main.py to the log file and run it in the background
    (python3 "$parent_directory/main.py" >> "$log_file" 2>&1 &)

    # Optionally, you can add a sleep to give it some time to start
    sleep 5

    echo "main.py started in the background. Logs are in $log_file"
else
    echo "main.py not found in the parent directory."
fi
