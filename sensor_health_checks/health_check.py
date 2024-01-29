import requests
import time
import subprocess
import logging

class HealthChecker:

    def __init__(self):
        pass
        
    def checkInternetConnection(self, ):
        url = "http://google.com/"
        timeout = 3
        
        while True:
            try:
                # Requesting URL
                request = requests.get(url, timeout=timeout)
                return True
            
            except (requests.ConnectionError, requests.Timeout) as exception:
                # restart network services
                logging.error('network connection failed, restarting wpa_supplicant service')
                subprocess.run(['systemctl', 'restart', 'wpa_supplicant'], check=True)
                time.sleep(5) 
            