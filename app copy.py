from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from geopy.geocoders import Nominatim
from geopy.point import Point
import random

app = Flask(__name__)
CORS(app)

def generate_random_coordinates(region, timezone):
    geolocator = Nominatim(user_agent="my-app")
    location = geolocator.geocode(region)
    if location is None:
        return jsonify({'error': 'Failed to retrieve location data for the region.'}), 400

    min_lat, max_lat = location.point[0] - 1, location.point[0] + 1
    min_lon, max_lon = location.point[1] - 1, location.point[1] + 1

    random_lat = random.uniform(min_lat, max_lat)
    random_lon = random.uniform(min_lon, max_lon)

    result = {
        'latitude': random_lat,
        'longitude': random_lon,
        'timezone' : timezone
    }

    return jsonify(result), 200

@app.route('/', methods=['GET'])
def get_random_coordinates():
    ip_address = request.args.get('ip')
    if ip_address is None:
        return jsonify({'error': 'Failed to retrieve ip adresse.'}), 400
    # Get IP region
    ip_info_url = f"https://ipapi.co/{ip_address}/region/"
    ip_timezone_url = f"https://ipapi.co/{ip_address}/timezone/"
    response = requests.get(ip_info_url)
    response_timezone = requests.get(ip_timezone_url)
    if response.status_code == 200:
        region = response.text.strip()
        timezone = response_timezone.text.strip()
    else:
        return jsonify({'error': 'Failed to retrieve region of the IP.'}), 400

    # Call the generate_random_coordinates function
    result = generate_random_coordinates(region, timezone)

    return result

if __name__ == '__main__':
    app.run()
