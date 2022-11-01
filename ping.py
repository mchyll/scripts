import requests
import time
import datetime


while True:
    response = requests.get("https://iot-app.azurewebsites.net/api/SensorData/Status")
    print(f"{datetime.datetime.now().time()}: {response.status_code} {response.reason}", end='\r')
    time.sleep(60)
