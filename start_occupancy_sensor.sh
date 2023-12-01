#!/bin/bash

# Run the enable_monitoring_mode.sh script
sudo bash setup/networking_setup/enable-monitor-mode.sh

# Run internet established script
sudo /usr/bin/python3 setup/networking_setup/internet_established.py
