from flask import Flask, render_template, request
from model.smart_devices import *
import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 40.4406,
	"longitude": -79.995888,
	"current": "temperature_2m",
	"hourly": "temperature_2m",
    "temperature_unit": "fahrenheit"
}

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below


app = Flask(__name__)
HOME = Home("4716 Ellsworth Ave", "devices.json")

# Initialize home
@app.route("/", methods=['GET'])
def index():
    response = openmeteo.weather_api(url, params=params)[0]
    current = response.Current()
    current_temp = current.Variables(0).Value()
    return render_template('load_up.html', home = HOME, temp = round(current_temp,2))

# Show all the devices
@app.route("/devices", methods=['GET'])
def devices():
    return render_template('devices.html', home = HOME)

# Creates a new device and adds it to home
@app.route('/post_json', methods=['POST'])
def post_json_data():
    post_data = request.get_json()
    if ("name" not in post_data) or ("location" not in post_data) \
        or ("power" not in post_data):
        print("Missing data to create device")
        return post_data
    else:
        location, name, power = post_data["location"], post_data["name"], post_data["power"]
        if name == "light":
            device = LightBulb(location, name, power)
        elif name == "vacuum":
            device = SmartVacuum(location, name, power)
        elif name == "thermostat":
            device = Thermostat(location, name, power)
        else:
            print("Not a supported device")
            return post_data
        HOME.add_device(device)
        HOME.save()
    return post_data

# Removing a device from the list
@app.route('/delete-device', methods=['DELETE'])
def remove_device():
    delete_data = request.get_json()
    if ("name" not in delete_data) or ("location" not in delete_data):
        print("Missing data to create device")
    else:
        name, location = delete_data["name"], delete_data["location"]
        HOME.delete(name, location)
        HOME.save()

# Turning a device on or off
@app.route('/update-device', methods=['PUT'])
def switch_power():
    put_data = request.get_json()
    if ("name" not in put_data) or ("location" not in put_data):
        print("missing data to switch a device power")
    else:
        name, location = put_data["name"], put_data["location"]
        HOME.swith_power(name, location)




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
    