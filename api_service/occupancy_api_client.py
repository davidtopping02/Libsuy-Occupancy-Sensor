import datetime
import logging
import requests


class OccupancyDataApiClient:
    def __init__(self, api_url="http://10.8.0.1:3000/occupancy/add"):
        self.api_url = api_url

    def submit_occupancy_data(self, sensor_id, occupancy_count):

        # current timestamp in MySQL format
        current_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        payload = {
            'sensor_id': sensor_id,
            'timestamp': current_timestamp,
            'occupancy_count': occupancy_count
        }

        try:
            response = requests.post(self.api_url, json=payload)
            if response.status_code == 200:
                logging.info("Data successfully posted to the API.")
            else:
                error_message = f"Error with status code {response.status_code}. "
                if response.status_code == 400:
                    error_message += "Bad request. Check your payload data."
                elif response.status_code == 404:
                    error_message += "API endpoint not found."
                elif response.status_code == 500:
                    error_message += "Internal server error on the API."
                else:
                    error_message += "Unexpected response status code."

                # log the error message along with the payload for more context
                logging.error(f"{error_message} Payload: {payload}")

        except requests.exceptions.RequestException as e:
            # log the exception along with the payload
            logging.error(f"An error occurred: {e}. Payload: {payload}")
