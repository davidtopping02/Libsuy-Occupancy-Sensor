import fcntl
import socket
import struct
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
                logging.info("internet established")
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
                    logging.info(f"{monitoring_interface} in monitoring mode")
                    return True
                else:
                    logging.error(
                    'No monitoring mode interface found, running enable-monitoring-mode.sh')
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

    def get_sensor_id(self):
        try:
            # Create a socket object for IPv4
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            # Use ioctl to get the IP address associated with the 'tun0' interface
            ip_address = socket.inet_ntoa(fcntl.ioctl(
                sock.fileno(),
                0x8915,  # SIOCGIFADDR
                struct.pack('256s', b'tun0')[:32]
            )[20:24])
            
            logging.info(f"sensor id retrieved: {ip_address}")
            return ip_address
        except Exception as e:
            logging.error(f"Error: {e}")
            return None