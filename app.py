from flask import Flask, request, jsonify
from flask_cors import CORS
# import requests
from geopy.geocoders import Nominatim
from geopy.point import Point
import random
from timezonefinder import TimezoneFinder

app = Flask(__name__)
CORS(app)

def generate_random_coordinates(region):
    geolocator = Nominatim(user_agent="my-app")
    location = geolocator.geocode(region)
    if location is None:
        return jsonify({'error': 'Failed to retrieve location data for the region.'}), 400

    min_lat, max_lat = location.point[0] - 1, location.point[0] + 1
    min_lon, max_lon = location.point[1] - 1, location.point[1] + 1

    random_lat = random.uniform(min_lat, max_lat)
    random_lon = random.uniform(min_lon, max_lon)
    obj = TimezoneFinder()
    timezone = obj.timezone_at(lng=random_lon, lat=random_lat)

    result = {
        'latitude': random_lat,
        'longitude': random_lon,
        'region' : region,
        'timezone' : timezone
    }

    return jsonify(result), 200

@app.route('/', methods=['GET'])
def get_random_coordinates():
    ip = request.args.get('ip')
    from ip2geotools.databases.noncommercial import DbIpCity
    response = DbIpCity.get(ip, api_key='free')
    region = response.region
    # Call the generate_random_coordinates function
    result = generate_random_coordinates(region)

    return result

if __name__ == '__main__':
    app.run(port = 8080, debug = True)
