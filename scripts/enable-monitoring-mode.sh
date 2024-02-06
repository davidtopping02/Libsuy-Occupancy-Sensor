#!/bin/bash

# Check if the script is run as root
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root. Please use sudo or run as root."
    exit 1
fi

# Set the wireless interface to wlan1
interface="wlan1"

# Check if airmon-ng is installed
if ! command -v airmon-ng &>/dev/null; then
    echo "Error: airmon-ng not found. Please install the aircrack-ng package."
    exit 1
fi

# Put the interface into monitoring mode using airmon-ng
echo "Putting $interface into monitoring mode..."
airmon-ng start "$interface"

# Check if the operation was successful
if [ $? -eq 0 ]; then
    echo "Monitoring mode enabled on $interface."
else
    echo "Failed to enable monitoring mode on $interface."
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

exit 0
