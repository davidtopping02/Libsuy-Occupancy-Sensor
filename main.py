import asyncio
import datetime
import logging
import os
from occupancy_counting.package_scanner import PackageScanner
from api_service.occupancy_api_client import OccupancyDataApiClient
from sensor_health_checks.health_check import HealthChecker


class OccupancySensor:

    def __init__(self, monitoring_interface="wlan1mon"):
        self.monitoring_interface = monitoring_interface
        self.network_traffic_scanner = PackageScanner(
            self.monitoring_interface)
        self.occupancy_api_client = OccupancyDataApiClient()
        self.health_checker = HealthChecker()

    def configure_logging(self, log_directory="logs/"):
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)
        datetime_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_file = f'{log_directory}+{datetime_str}.log'
        logging.basicConfig(level=logging.INFO, filename=log_file,
                            filemode='w', format='%(levelname)s:[%(asctime)s]:%(name)s: %(message)s')

    async def get_current_occupancy(self):
        scan_duration = 5
        return await self.network_traffic_scanner.scan(scan_duration)

    async def run_sensor_lifecycle(self):
        self.occupancy_api_client.submit_occupancy_data('10.8.0.3', 100)
        self.health_checker.check_internet_connection()
        self.health_checker.check_monitoring_mode_network_interfaces(
            self.monitoring_interface)

        while True:
            scan_result = await self.get_current_occupancy()
            print(scan_result)


if __name__ == "__main__":
    print("START")
    sensor = OccupancySensor()
    sensor.configure_logging()
    asyncio.run(sensor.run_sensor_lifecycle())
    print("END")
