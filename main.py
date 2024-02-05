import asyncio
import datetime
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

    def configure_logging(self, log_directory="logs/"):
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
        scan_duration = 5
        return await self.network_traffic_scanner.scan(scan_duration)

    async def run_sensor_lifecycle(self):

        self.health_checker.check_internet_connection()
        self.sensor_id = self.health_checker.get_sensor_id()
        self.health_checker.check_monitoring_mode_network_interfaces(
            self.monitoring_interface)

        while True:
            scan_result = await self.get_current_occupancy()
            self.occupancy_api_client.submit_occupancy_data(
                self.sensor_id, scan_result)


if __name__ == "__main__":
    sensor = OccupancySensor()
    sensor.configure_logging()
    logging.info("START SENSOR")
    asyncio.run(sensor.run_sensor_lifecycle())
    logging.info("END SENSOR")
