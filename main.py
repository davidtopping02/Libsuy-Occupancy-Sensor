import asyncio
from datetime import datetime, timedelta
import logging
import os
from occupancy_counting.package_scanner import PackageScanner
from api_service.occupancy_api_client import OccupancyDataApiClient
from sensor_health_checks.health_check import HealthChecker


class OccupancySensor:

    def __init__(self):
        # initialise local objects
        self.monitoring_interface = "wlan1mon"
        self.sensor_id = None
        self.network_traffic_scanner = PackageScanner(
            self.monitoring_interface)
        self.occupancy_api_client = OccupancyDataApiClient()
        self.health_checker = HealthChecker()

    def configure_logging(self, log_directory="/home/pi/UOD-Occupancy-Sensor/logs/"):
        # create log directory if it doesn't exist
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)

        # generate a log file name with the current date
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        log_file = f'{log_directory}{current_date}.log'

        # configure logging with the log file and format
        logging.basicConfig(level=logging.INFO, filename=log_file,
                            filemode='a', format='%(levelname)s:[%(asctime)s]:%(name)s: %(message)s')

    async def get_current_occupancy(self):
        scan_duration = 20
        return await self.network_traffic_scanner.scan(scan_duration)

    async def run_sensor_lifecycle(self):

        while True:
            sensor.configure_logging()
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
                    logging.info(
                        "END SENSOR - breaking main loop. Goodnight.")
                    # exit the inner loop
                    break


if __name__ == "__main__":
    sensor = OccupancySensor()
    asyncio.run(sensor.run_sensor_lifecycle())
