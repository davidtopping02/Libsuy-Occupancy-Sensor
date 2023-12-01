#!/bin/bash

### setup WiFi Connection to eduroam ###
eduroam_setup() {
    echo "Copying files for eduroam setup..."

    # Check if interfaces file exists before copying
    if [ -e "./configuration-files/interfaces" ]; then
        sudo cp --no-clobber ./configuration-files/interfaces /etc/network/interfaces
    else
        echo "Error: ./configuration-files/interfaces not found."
        exit 1
    fi

    # Check if wpa_supplicant.conf file exists before copying
    if [ -e "./configuration-files/wpa_supplication.conf" ]; then
        sudo cp --no-clobber ./configuration-files/wpa_supplication.conf /etc/wpa_supplicant/wpa_supplicant.conf
    else
        echo "Error: ./configuration-files/wpa_supplication.conf not found."
        exit 1
    fi

    echo "Restarting network services..."

    # Restart networking service and check for errors
    sudo systemctl restart networking
    if [ $? -eq 0 ]; then
        echo "Networking service restarted successfully."
    else
        echo "Error: Failed to restart networking service."
        exit 1
    fi

    # Restart wpa_supplicant service and check for errors
    sudo systemctl restart wpa_supplicant
    if [ $? -eq 0 ]; then
        echo "wpa_supplicant service restarted successfully."
    else
        echo "Error: Failed to restart wpa_supplicant service."
        exit 1
    fi
}

### setup ssh and network connection notification  ###



### entry point ###
echo "STARTING OCCUPANCY SENSOR SETUP"
eduroam_setup

echo "FINISHED"
