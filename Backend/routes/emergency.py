from flask import Blueprint, jsonify, request
import csv
import json
import os
from math import radians, sin, cos, sqrt, atan2

# Create blueprint
emergency_blueprint = Blueprint('emergency', __name__)

# Paths for CSV and JSON
EMERGENCY_SERVICES_FILE_PATH = os.path.join(os.path.dirname(__file__), 'emergency_services_data.json')
TRAVEL_CSV_PATH = os.path.join(os.path.dirname(__file__), 'travel.csv')

# Function to load emergency services from the new JSON file
def load_emergency_services():
    if os.path.exists(EMERGENCY_SERVICES_FILE_PATH):
        with open(EMERGENCY_SERVICES_FILE_PATH, 'r') as f:
            return json.load(f)
    return None

# Function to load city data from the travel.csv
def load_city_data():
    cities = []
    try:
        with open(TRAVEL_CSV_PATH, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                city = {
                    "city_name": row["city_name"],
                    "latitude": float(row["latitude"]),
                    "longitude": float(row["longitude"])
                }
                cities.append(city)
    except Exception as e:
        print(f"Error reading CSV: {e}")
    return cities

# Haversine formula to calculate distance between two points (in kilometers)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in kilometers
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c  # Distance in kilometers

# Function to get nearby emergency services based on user's location
@emergency_blueprint.route('/', methods=['GET'])
def get_emergency_services():
    """Fetch emergency services based on the user's location and compare with city data."""
    
    # Get user's location from query params
    try:
        user_lat = float(request.args.get('lat'))  # User's Latitude
        user_lon = float(request.args.get('lon'))  # User's Longitude
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid or missing location parameters"}), 400
    
    # Load city data from CSV
    cities = load_city_data()

    nearby_cities = []

    # Compare each city with the user's location and calculate distance
    for city in cities:
        distance = haversine(user_lat, user_lon, city['latitude'], city['longitude'])
        if distance <= 50:  # Threshold of 50 km for nearby cities (can be adjusted)
            nearby_cities.append({
                "city_name": city['city_name'],
                "distance_km": distance
            })

    if not nearby_cities:
        return jsonify({"error": "No nearby cities found based on your location."}), 404

    # Load emergency services (can be cached in JSON)
    emergency_services = load_emergency_services()

    if emergency_services:
        # Filter emergency services based on nearby cities
        nearby_emergency_services = []
        for service in emergency_services:
            for city in nearby_cities:
                if service['city_name'] == city['city_name']:
                    nearby_emergency_services.append(service)
        
        if nearby_emergency_services:
            return jsonify(nearby_emergency_services)
        
    return jsonify({"error": "No emergency services found for nearby cities."}), 404
