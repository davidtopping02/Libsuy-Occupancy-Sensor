#!/bin/bash

# Check if the script is run as root
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root. Please use sudo or run as root."
    exit 1
fi

# Check if the wireless interface is provided as an argument
if [ -z "$1" ]; then
    echo "Usage: $0 <interface>"
    exit 1
fi

interface="$1"

# Check if the interface exists
if ! iw dev "$interface" info &>/dev/null; then
    echo "Error: Interface $interface not found."
    exit 1
fi

# Check if airmon-ng is installed
if ! command -v airmon-ng &>/dev/null; then
    echo "Error: airmon-ng not found. Please install aircrack-ng package."
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

exit 0
