from flask import Flask, request, jsonify
import phonenumbers
from phonenumbers import geocoder, carrier
from opencage.geocoder import OpenCageGeocode
import requests

# API Keys
OPENCAGE_API_KEY = "9d9e343d24be43e39d67cae48be53d65"
NUMLOOKUP_API_URL = "https://www.numlookupapi.com/api/v1/lookup?number={}"

# Initialize APIs
geocode = OpenCageGeocode(OPENCAGE_API_KEY)

app = Flask(__name__)

@app.route('/')
def home():
    return "Truecaller API by @AzR_projects"

@app.route('/get_number_info', methods=['GET'])
def get_number_info():
    number = request.args.get('number')
    if not number:
        return jsonify({
            "status": "error",
            "message": "❌ Phone number required! Please provide a valid number.",
            "credit": "@AzR_projects"
        }), 400

    try:
        # Ensure number starts with '+'
        if not number.startswith('+'):
            number = '+' + number

        check_number = phonenumbers.parse(number, None)
        number_location = geocoder.description_for_number(check_number, "en")
        service_provider = carrier.name_for_number(check_number, "en")

        # Get name using NumLookup API
        name_lookup_url = NUMLOOKUP_API_URL.format(number)
        name_response = requests.get(name_lookup_url).json()
        name = name_response.get("name", "Unknown")

        # Geocoding location
        results = geocode.geocode(str(number_location))
        if not results:
            return jsonify({
                "status": "error",
                "message": "❌ Location details not found for this number.",
                "credit": "@AzR_projects"
            }), 404

        lat = results[0]['geometry']['lat']
        lng = results[0]['geometry']['lng']
        timezone = results[0]['annotations']['timezone']['name']
        currency_name = results[0]['annotations']['currency']['name']
        currency_symbol = results[0]['annotations']['currency']['symbol']

        return jsonify({
            "status": "success",
            "message": "✅ Phone number details retrieved successfully!",
            "number": number,
            "name": name,
            "location": number_location,
            "latitude": lat,
            "longitude": lng,
            "service_provider": service_provider,
            "timezone": timezone,
            "currency_name": currency_name,
            "currency_symbol": currency_symbol,
            "credit": "@AzR_projects"
        })

    except phonenumbers.NumberParseException:
        return jsonify({
            "status": "error",
            "message": "❌ Invalid phone number format! Please check and try again.",
            "credit": "@AzR_projects"
        }), 400

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"❌ An unexpected error occurred: {str(e)}",
            "credit": "@AzR_projects"
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
    
