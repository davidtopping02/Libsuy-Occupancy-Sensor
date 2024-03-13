# UOD Occupancy Sensor

## Description
The UOD Occupancy Sensor project uses a Raspberry Pi Zero W with RT5370 WLAN USB adapters to monitor space occupancy through MAC address scanning. It's designed for environments with dense device presence, providing real-time occupancy insights.

## Hardware Setup
- Raspberry Pi Zero W with 128GB SD card
- Micro USB to USB A adapter connected to a USB hub
- Two RT5370 WLAN USB adapters for monitoring and internet connectivity

## Software Requirements
- Raspberry Pi OS Lite (Bullseye)
- Python 3 (see `requirements.txt` for dependencies)

## Installation
1. Flash Raspberry Pi OS Lite onto the SD card.
2. Connect the hardware as per the setup above.
3. Clone this repository to your Raspberry Pi.
4. Install Python dependencies:
   `pip install -r requirements.txt`

## Configuration
Configure both WLAN adapters:
One for monitoring WiFi traffic in promiscuous mode.
Another for stable internet access, particularly in environments with dense wireless traffic.

## Usage
Execute the main.py script to start the occupancy detection:
`python3 main.py`
