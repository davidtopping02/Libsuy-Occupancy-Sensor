#!/bin/bash

# Get the current directory
current_directory="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if main.py exists in the current directory
if [ -e "$current_directory/main.py" ]; then
    # Run main.py with sudo
    sudo python3 "$current_directory/main.py"
else
    echo "main.py not found in the current directory."
fi
