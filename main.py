import asyncio
import sys
from datetime import datetime, timedelta
import logging
import os
from occupancy_counting.package_scanner import PackageScanner
from api_service.occupancy_api_client import OccupancyDataApiClient
from sensor_health_checks.health_check import HealthChecker


class OccupancySensor:
    def __init__(self, scan_duration=20):
        # initialise local objects
        self.monitoring_interface = "wlan1mon"
        self.sensor_id = None
        self.network_traffic_scanner = PackageScanner(
            self.monitoring_interface)
        self.occupancy_api_client = OccupancyDataApiClient()
        self.health_checker = HealthChecker()
        self.scan_duration = scan_duration

    def configure_logging(self, log_directory="/home/pi/UOD-Occupancy-Sensor/logs/"):
        # create log directory if it doesn't exist
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)

        # generate a log file name with the current date
        current_date = datetime.now().strftime("%Y-%m-%d")
        log_file = f'{log_directory}{current_date}.log'

        # configure logging with the log file and format
        logging.basicConfig(level=logging.INFO, filename=log_file,
                            filemode='a', format='%(levelname)s:[%(asctime)s]:%(name)s: %(message)s')

    def reboot_system(self):
        logging.info("Initiating daily system reboot")
        os.system('sudo reboot')

    async def get_current_occupancy(self):
        return await self.network_traffic_scanner.scan(self.scan_duration)

    async def run_sensor_lifecycle(self):
        while True:
            self.configure_logging()
            logging.info("START SENSOR")

            now = datetime.now()
            end_of_day = datetime(now.year, now.month,
                                  now.day) + timedelta(days=1)

            while True:
                self.health_checker.check_connection()
                self.sensor_id = self.health_checker.get_sensor_id()
                self.health_checker.check_monitoring_mode_network_interfaces(
                    self.monitoring_interface)

                scan_result = await self.get_current_occupancy()
                self.occupancy_api_client.submit_occupancy_data(
                    self.sensor_id, scan_result)

                if datetime.now() >= end_of_day:
                    logging.info("END SENSOR - breaking main loop. Goodnight.")
                    self.reboot_system()
                    break


if __name__ == "__main__":
    # check if a scan duration was provided as a command-line argument
    if len(sys.argv) > 1:
        try:
            scan_duration = int(sys.argv[1])
        except ValueError:
            print("Invalid scan duration provided. Using default value.")
            scan_duration = 20
    else:
        scan_duration = 20

    sensor = OccupancySensor(scan_duration=scan_duration)
    asyncio.run(sensor.run_sensor_lifecycle())
