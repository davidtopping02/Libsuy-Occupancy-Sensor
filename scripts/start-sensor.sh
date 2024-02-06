#!/bin/bash

# Check if the script is run as root
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root. Please use sudo or run as root."
    exit 1
fi

# Get the parent directory of the current directory
parent_directory="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && cd .. && pwd )"

# Check if main.py exists in the parent directory
if [ -e "$parent_directory/main.py" ]; then
    # Run main.py with sudo
    python3 "$parent_directory/main.py"
else
    echo "main.py not found in the parent directory."
fi
