# external imports
import asyncio
import datetime
import logging
import os


# internal modules
from occupancy_counting.package_scanner import PackageScanner
from database_service.mariaDb import DatabaseManager
from sensor_health_checks.health_check import HealthChecker


class OccupancySensor():

    # Constructor to initialize the PackageScanner and DatabaseManager
    def __init__(self, monitoring_interface="wlan1mon"):
        
        self.monitoring_interface = monitoring_interface
        self.network_traffic_scanner = PackageScanner(self.monitoring_interface)
        self.db_manager = DatabaseManager('occupancySensorLog.txt')
        self.health_cheker = HealthChecker()

    def loggingConfig(self, log_directory = "logs/"):
        
        # Ensure the log directory exists, create it if not
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)

        # Configure logging with the dynamic log file name
        datetime_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        logging.basicConfig(level=logging.INFO, filename=f'{log_directory}+{datetime_str}.log', filemode='w', format='%(levelname)s:[%(asctime)s]:%(name)s: %(message)s')


    # Asynchronous method to get the current occupancy by scanning network traffic
    async def getCurrentOccupancy(self):

        scan_duration = 5
        return await self.network_traffic_scanner.scan(scan_duration)

    async def runSensorLifeCycle(self):

        # sensor health checks
        self.health_cheker.checkInternetConnection()
        self.health_cheker.checkMonitoringModeNetworkInterfaces(self.monitoring_interface)

        while True:
            scanTask = await sensor.getCurrentOccupancy()
            print(scanTask)
            # self.db_manager.append_to_file(output_line)


    

if __name__ == "__main__":

    print("START")
    sensor = OccupancySensor()
    sensor.loggingConfig()
    asyncio.run(sensor.runSensorLifeCycle())
    print("END")