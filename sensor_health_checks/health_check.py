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

                interface = "wlan0"

                # if internet connection is not available, restart network services
                logging.error(
                    f'Network connection failed, restarting {interface}')

                # restart wireless interface
                subprocess.run(["sudo", "ifdown", interface], check=True)
                subprocess.run(["sudo", "ifup", interface], check=True)

                # restart openvpn client service
                subprocess.run(["sudo", "systemctl", "restart",
                               "openvpn@client"], check=True)

                time.sleep(self.waitDuration)

    def checkMonitoringModeNetworkInterfaces(self, monitoring_interface):
        while True:
            try:
                # check if the specified network interface is in monitoring mode
                result = subprocess.run(
                    ['iwconfig', monitoring_interface], capture_output=True, text=True, check=True)

                # check if the output contains "Mode: Monitor"
                if "Mode" in result.stdout and "Monitor" in result.stdout:
                    return True
                else:
                    self.runEnableMonitoringMode()

            except subprocess.CalledProcessError:
                # if the 'iwconfig' command fails, run the function to enable monitoring mode
                self.runBashScript('enable-monitoring-mode.sh')
                logging.error(
                    'No monitoring mode interface found, running enable-monitoring-mode.sh')
                time.sleep(self.waitDuration)

    def runBashScript(self, scriptLocation):
        try:
            subprocess.run(['sh', scriptLocation], check=True)
        except subprocess.CalledProcessError as e:
            logging.error(f'Failed to run {scriptLocation}')
