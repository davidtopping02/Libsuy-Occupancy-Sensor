from occupancy_counting.package_scanner import PackageScanner
from database_service.mariaDb import DatabaseManager
import asyncio

class OccupancySensor():

    # Constructor to initialize the PackageScanner and DatabaseManager
    def __init__(self):

        self.network_traffic_scanner = PackageScanner("wlp2s0")
        self.db_manager = DatabaseManager('occupancySensorLog.txt')

    # Asynchronous method to get the current occupancy by scanning network traffic
    async def getCurrentOccupancy(self):

        scan_duration = 0.1
        return await self.network_traffic_scanner.scan(scan_duration)

    # Asynchronous method to run the lifecycle of the occupancy sensor
    async def runSensorLifeCycle(self):
        
        while True:
            scanTask = await sensor.getCurrentOccupancy()
            print(scanTask)
            # Appending a new line to the specified text file using the DatabaseManager
            self.db_manager.append_to_file(str(scanTask))

# Entry point of the script
if __name__ == "__main__":

    print("START")
    sensor = OccupancySensor()
    asyncio.run(sensor.runSensorLifeCycle())
    print("END")
