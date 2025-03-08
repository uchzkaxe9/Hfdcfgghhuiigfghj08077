from flask import Flask, request, jsonify, send_file
import phonenumbers
from phonenumbers import geocoder, carrier
from opencage.geocoder import OpenCageGeocode
import folium
import os

# OpenCage API key
OPENCAGE_API_KEY = "9d9e343d24be43e39d67cae48be53d65"
geocode = OpenCageGeocode(OPENCAGE_API_KEY)

app = Flask(__name__)

@app.route('/')
def home():
    return "Phone Number Tracker API is running!"

@app.route('/get_number_info', methods=['GET'])
def get_number_info():
    number = request.args.get('number')
    if not number:
        return jsonify({"error": "Phone number required"}), 400

    try:
        check_number = phonenumbers.parse(number)
        number_location = geocoder.description_for_number(check_number, "en")
        service_provider = carrier.name_for_number(check_number, "en")

        # Geocoding location
        results = geocode.geocode(str(number_location))
        if not results:
            return jsonify({"error": "Location not found"}), 404

        lat = results[0]['geometry']['lat']
        lng = results[0]['geometry']['lng']
        timezone = results[0]['annotations']['timezone']['name']
        currency_name = results[0]['annotations']['currency']['name']
        currency_symbol = results[0]['annotations']['currency']['symbol']
        flag = results[0]['annotations']['flag']

        # Map generation
        map_location = folium.Map(location=[lat, lng], zoom_start=8)
        folium.Marker([lat, lng], popup=number_location).add_to(map_location)
        
        map_path = "mylocation.html"
        map_location.save(map_path)

        return jsonify({
            "number": number,
            "location": number_location,
            "service_provider": service_provider,
            "timezone": timezone,
            "currency_name": currency_name,
            "currency_symbol": currency_symbol,
            "flag": flag,
            "latitude": lat,
            "longitude": lng,
            "map_url": f"https://your-render-app-url.onrender.com/map"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/map')
def get_map():
    map_path = "mylocation.html"
    if os.path.exists(map_path):
        return send_file(map_path)
    else:
        return jsonify({"error": "Map not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
