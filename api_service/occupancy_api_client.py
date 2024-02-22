import json
import logging
import requests


class OccupancyDataApiClient:
    def __init__(self, api_url="http://10.8.0.1:80/occupancy/add", config_file="/home/pi/UOD-Occupancy-Sensor/config.json"):
        self.api_url = api_url
        with open(config_file) as f:
            config = json.load(f)
        self.api_key = config["api_key"]

    def submit_occupancy_data(self, sensor_id, occupancy_count):
        payload = {
            'sensor_id': sensor_id,
            'occupancy_count': occupancy_count
        }

        # Define headers including the API key
        headers = {
            'X-API-Key': self.api_key,
        }

        try:
            # Include headers in the POST request
            response = requests.post(
                self.api_url, json=payload, headers=headers)
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

                logging.error(f"{error_message} Payload: {payload}")

        except requests.exceptions.RequestException as e:
            logging.error(f"An error occurred: {e}. Payload: {payload}")
