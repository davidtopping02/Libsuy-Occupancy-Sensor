import requests
import time
import subprocess
import logging

class HealthChecker:

    def __init__(self):
        self.waitDuration = 60

    def checkInternetConnection(self):
        url = "http://google.com/"
        timeout = 3

        while True:
            try:
                # requesting URL to check internet connection
                request = requests.get(url, timeout=timeout)
                return True

            except (requests.ConnectionError, requests.Timeout) as exception:
                # ff internet connection is not available, restart network services
                logging.error('Network connection failed, restarting wpa_supplicant service')
                subprocess.run(['systemctl', 'restart', 'wpa_supplicant'], check=True)
                time.sleep(self.waitDuration)

    def checkMonitoringModeNetworkInterfaces(self, monitoring_interface):
        while True:
            try:
                # check if the specified network interface is in monitoring mode
                result = subprocess.run(['iwconfig', monitoring_interface], capture_output=True, text=True, check=True)

                # check if the output contains "Mode: Monitor"
                if "Mode" in result.stdout and "Monitor" in result.stdout:
                    return True
                else:
                    self.runEnableMonitoringMode()

            except subprocess.CalledProcessError:
                # if the 'iwconfig' command fails, run the function to enable monitoring mode
                self.runEnableMonitoringMode()
                logging.error('No monitoring mode interface found, running start_occupancy_sensor.sh')
                time.sleep(self.waitDuration)

    def runEnableMonitoringMode(self):
        # run script to enable monitoring mode for the specified network interface
        try:
            subprocess.run(['sh', 'start_occupancy_sensor.sh'], check=True)
        except subprocess.CalledProcessError as e:
            logging.error('Failed to run start_occupancy_sensor.sh')
