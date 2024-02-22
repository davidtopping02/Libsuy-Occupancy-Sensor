import fcntl
import socket
import struct
import time
import subprocess
import logging


class HealthChecker:
    def __init__(self):
        self.wait_duration = 60

    def check_connection(self):
        ip_address = "10.8.0.1"
        count = 4  # Number of ping attempts

        while True:
            try:
                # ping the raspberry pi controller
                subprocess.check_output(
                    ["ping", "-c", str(count), ip_address], stderr=subprocess.STDOUT)
                logging.info("Connection established")
                return True

            except subprocess.CalledProcessError as e:
                interface = "wlan0"
                logging.error(
                    f'Ping {ip_address} failed, restarting wpa_supplicant.service')

                # restart the network interface and OpenVPN
                subprocess.run(["sudo", "systemctl", "restart",
                               "wpa_supplicant"], check=True)
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
                self.run_bash_script('/scripts/enable-monitoring-mode.sh')
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
