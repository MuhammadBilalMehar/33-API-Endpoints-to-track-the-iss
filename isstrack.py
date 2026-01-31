import requests
from datetime import datetime

API_URL = "http://api.open-notify.org/iss-now.json"

response = requests.get(API_URL)

if response.status_code == 200:
    data = response.json()

    latitude = data["iss_position"]["latitude"]
    longitude = data["iss_position"]["longitude"]
    timestamp = data["timestamp"]

    time = datetime.fromtimestamp(timestamp)

    print("🛰 ISS Current Location")
    print("----------------------")
    print(f"Latitude : {latitude}")
    print(f"Longitude: {longitude}")
    print(f"Time     : {time}")
else:
    print("Failed to fetch ISS data")
