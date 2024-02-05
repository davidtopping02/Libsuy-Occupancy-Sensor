import requests
import time
import subprocess
import logging


class HealthChecker:
    def __init__(self):
        self.wait_duration = 60

    def check_internet_connection(self):
        url = "http://google.com/"
        timeout = 3

        while True:
            try:
                response = requests.get(url, timeout=timeout)
                return True

            except (requests.ConnectionError, requests.Timeout) as exception:
                interface = "wlan0"

                logging.error(
                    f'Network connection failed, restarting {interface}')

                subprocess.run(["sudo", "ifdown", interface], check=True)
                subprocess.run(["sudo", "ifup", interface], check=True)
                subprocess.run(["sudo", "systemctl", "restart",
                               "openvpn@client"], check=True)

                time.sleep(self.wait_duration)

    def check_monitoring_mode_network_interfaces(self, monitoring_interface):
        while True:
            try:
                result = subprocess.run(
                    ['iwconfig', monitoring_interface], capture_output=True, text=True, check=True)

                if "Mode" in result.stdout and "Monitor" in result.stdout:
                    return True
                else:
                    self.run_bash_script('enable-monitoring-mode.sh')

            except subprocess.CalledProcessError:
                self.run_bash_script('enable-monitoring-mode.sh')
                logging.error(
                    'No monitoring mode interface found, running enable-monitoring-mode.sh')
                time.sleep(self.wait_duration)

    def run_bash_script(self, script_location):
        try:
            subprocess.run(['sh', script_location], check=True)
        except subprocess.CalledProcessError as e:
            logging.error(f'Failed to run {script_location}')
