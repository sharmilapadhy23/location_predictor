import csv
import subprocess
from geopy.geocoders import Nominatim

def save_prediction(user_id, latitude, longitude, location_name):
    """Save the predicted location into PostgreSQL."""
    try:
        command = [
            "psql",
            "-U", "postgres",
            "-h", "localhost",
            "-d", "location_db",
            "-c", f"INSERT INTO location_predictions (user_id, predicted_latitude, predicted_longitude, location_name) VALUES ('{user_id}', {latitude}, {longitude}, '{location_name}');"
        ]
        subprocess.run(command, capture_output=True, text=True, check=True)
        print(f"✅ Prediction saved for User {user_id}: {location_name}")
    except subprocess.CalledProcessError as e:
        print("❌ Error saving prediction:", e.stderr)

def get_location_name(latitude, longitude):
    """Get the location name from latitude and longitude."""
    geolocator = Nominatim(user_agent="geo_predictor")
    location = geolocator.reverse((latitude, longitude), exactly_one=True)
    return location.address if location else "Unknown Location"

def predict_next_location(csv_file, user_id):
    """Predicts the next location and saves it in the database."""
    last_locations = []

    with open(csv_file, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header

        for row in reader:
            if row[0] == str(user_id):
                latitude, longitude = float(row[1]), float(row[2])
                last_locations.append((latitude, longitude))

    if not last_locations:
        print(f"❌ No location data found for User {user_id}.")
        return None

    if len(last_locations) < 2:
        last_lat, last_long = last_locations[-1]
    else:
        last_lat = sum(lat for lat, _ in last_locations[-5:]) / len(last_locations[-5:])
        last_long = sum(lon for _, lon in last_locations[-5:]) / len(last_locations[-5:])
    
    location_name = get_location_name(last_lat, last_long)
    print(f"✅ Predicted Next Location for User {user_id}: {last_lat}, {last_long} ({location_name})")
    save_prediction(user_id, last_lat, last_long, location_name)
    return last_lat, last_long, location_name

# Example Usage
csv_file = "../data/processed_data.csv"
predict_next_location(csv_file, user_id="0")  # Adjust user_id as needed