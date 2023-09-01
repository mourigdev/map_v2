from flask import Flask, request, jsonify
from flask_cors import CORS
# import requests
from geopy.geocoders import Nominatim
from geopy.point import Point
import random
from timezonefinder import TimezoneFinder
import ip2asn

app = Flask(__name__)
CORS(app)


import pycountry

import random
from geopy.geocoders import Nominatim

def get_random_region(country_code, preferred_language="en"):
    geolocator = Nominatim(user_agent="my-app")

    try:
        # Query Nominatim for administrative boundaries within the country
        query = f"{country_code},administrative"
        results = geolocator.geocode(query, exactly_one=False, language=preferred_language)

        if results:
            random_result = random.choice(results)
            # Extract only the region name from the display name
            region_name = random_result.raw['display_name'].split(',')[0].strip()
            return region_name
        return None  # Return None if no regions were found
    except Exception as e:
        return None  # Return None on error

def generate_random_coordinates_countrycode(country_code):
    region = get_random_region(country_code)
    if region is None:
        return jsonify({'error': 'Failed to retrieve region data for the country code.'}), 400

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
        'region': region,
        'timezone': timezone,
        'asn_country' : country_code
    }

    return jsonify(result), 200


def generate_random_coordinates(region, asn, country):
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
        'timezone' : timezone,
        'asn' : asn,
        'country' : country
    }

    return jsonify(result), 200

@app.route('/', methods=['GET'])
def get_random_coordinates():
    ip = request.args.get('ip')
    from ip2geotools.databases.noncommercial import DbIpCity
    response = DbIpCity.get(ip, api_key='free')


    i2a = ip2asn.IP2ASN("data/ip2asn-v4.tsv")
    i2aresult = i2a.lookup_address(ip)
    # if(i2aresult["country"] == response.country):
    #     result = generate_random_coordinates(response.region,i2aresult["country"],response.country)
    # # Call the generate_random_coordinates function
    # else:
    # result = generate_random_coordinates_countrycode(i2aresult["country"])
    result = generate_random_coordinates(response.region,i2aresult,response.country)

    return result

if __name__ == '__main__':
    app.run(port = 8080, debug = True)






# import random
# from geopy.geocoders import Nominatim

# def get_random_region(country_code, preferred_language="en"):
#     geolocator = Nominatim(user_agent="random_region_generator")

#     try:
#         # Query Nominatim for administrative boundaries within the country
#         query = f"{country_code},administrative"
#         results = geolocator.geocode(query, exactly_one=False, language=preferred_language)

#         if results:
#             random_result = random.choice(results)
#             # Extract only the region name from the display name
#             region_name = random_result.raw['display_name'].split(',')[0]
#             return {"region": region_name.strip()}
        
#         return {"error": "Country not found or has no regions."}
#     except Exception as e:
#         return {"error": str(e)}

# if __name__ == "__main__":
#     country_code = "RU"  # Replace with the ISO country code of your choice
#     preferred_language = "en"  # Replace with your preferred language code (e.g., "en" for English)
#     random_region = get_random_region(country_code, preferred_language)
#     geolocator = Nominatim(user_agent="my-app")
#     location = geolocator.geocode("Zelenogradsky Administrative Okrug")
