from occupancy_counting.package_scanner import PackageScanner
from database_service.mariaDb import DatabaseManager
import asyncio
import datetime

class OccupancySensor():

    # Constructor to initialize the PackageScanner and DatabaseManager
    def __init__(self):

        self.network_traffic_scanner = PackageScanner("wlan1mon")
        self.db_manager = DatabaseManager('occupancySensorLog.txt')

    # Asynchronous method to get the current occupancy by scanning network traffic
    async def getCurrentOccupancy(self):

        scan_duration = 5
        return await self.network_traffic_scanner.scan(scan_duration)

    async def runSensorLifeCycle(self):
        while True:
            scanTask = await sensor.getCurrentOccupancy()
            
            # Get the current date and time
            current_datetime = datetime.datetime.now()
            formatted_datetime = current_datetime.strftime('%H:%M:%S')
            
            # Combine date, time, and scanTask with commas and output it
            output_line = f"{formatted_datetime},{scanTask}"
            print(output_line)
            self.db_manager.append_to_file(output_line)

# Entry point of the script
if __name__ == "__main__":

    print("START")
    sensor = OccupancySensor()
    asyncio.run(sensor.runSensorLifeCycle())
    print("END")
