from flask import Flask, request, jsonify
import phonenumbers
from phonenumbers import geocoder, carrier
from opencage.geocoder import OpenCageGeocode

# OpenCage API key
OPENCAGE_API_KEY = "9d9e343d24be43e39d67cae48be53d65"
geocode = OpenCageGeocode(OPENCAGE_API_KEY)

app = Flask(__name__)

@app.route('/')
def home():
    return "Phone Number Tracker API by @AzR_projects is running!"

@app.route('/get_number_info', methods=['GET'])
def get_number_info():
    number = request.args.get('number')
    if not number:
        return jsonify({"error": "Phone number required", "credit": "@AzR_projects"}), 400

    try:
        # Agar number '+' ke bina hai, toh '+' auto-add kare
        if not number.startswith('+'):
            number = '+' + number

        check_number = phonenumbers.parse(number, None)  # Auto-detect country
        number_location = geocoder.description_for_number(check_number, "en")
        service_provider = carrier.name_for_number(check_number, "en")

        # Geocoding location
        results = geocode.geocode(str(number_location))
        if not results:
            return jsonify({"error": "Location not found", "credit": "@AzR_projects"}), 404

        lat = results[0]['geometry']['lat']
        lng = results[0]['geometry']['lng']
        timezone = results[0]['annotations']['timezone']['name']
        currency_name = results[0]['annotations']['currency']['name']
        currency_symbol = results[0]['annotations']['currency']['symbol']

        return jsonify({
            "number": number,
            "location": number_location,
            "latitude": lat,
            "longitude": lng,
            "service_provider": service_provider,
            "timezone": timezone,
            "currency_name": currency_name,
            "currency_symbol": currency_symbol,
            "credit": "@AzR_projects"
        })

    except Exception as e:
        return jsonify({"error": str(e), "credit": "@AzR_projects"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
    
