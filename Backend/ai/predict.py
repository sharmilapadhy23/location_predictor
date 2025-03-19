import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib
import requests
import os

# ✅ File paths
data_file = r"C:\Users\KIIT\Desktop\project\Location_Predictor\Backend\data\processed_travel_history.csv"
models_folder = r"C:\Users\KIIT\Desktop\project\Location_Predictor\Backend\models"
model_file = os.path.join(models_folder, "travel_model.pkl")
scaler_file = os.path.join(models_folder, "scaler.pkl")

# ✅ Ensure models folder exists
os.makedirs(models_folder, exist_ok=True)

# ✅ Verify the CSV file exists
if not os.path.exists(data_file):
    print(f"❌ Error: File not found at {data_file}")
    exit()

# ✅ Load dataset
df = pd.read_csv(data_file)

# ✅ Prepare features and target
features = ['Origin_Lat', 'Origin_Lon', 'distance_km']
target = ['Dest_Lat', 'Dest_Lon']

X = df[features]
y = df[target]

# ✅ Scale the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ✅ Train and save model + scaler if they don't exist
if not os.path.exists(model_file) or not os.path.exists(scaler_file):
    print("🔧 Training model and saving it...")
    
    # 🔥 Train the model
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_scaled, y)
    
    # 🔥 Save the model and scaler
    joblib.dump(rf_model, model_file)
    joblib.dump(scaler, scaler_file)
    print(f"✅ Model saved at {model_file}")
    print(f"✅ Scaler saved at {scaler_file}")
else:
    print("✅ Model and scaler already exist. Loading them...")

# ✅ Load the model and scaler
rf_model = joblib.load(model_file)
scaler = joblib.load(scaler_file)

# ✅ Function to get location names using OpenStreetMap API
def get_location_name(lat, lon):
    """Get location name from lat/lon using OpenStreetMap API."""
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
        headers = {'User-Agent': 'LocationPredictor/1.0'}
        response = requests.get(url, headers=headers, timeout=5)

        if response.status_code == 200:
            data = response.json()
            location_name = data.get('display_name', 'Unknown Location')
            return location_name
        else:
            print(f"❌ Error: Failed to fetch location for {lat}, {lon}")
            return "Unknown Location"
    except Exception as e:
        print(f"❌ Exception: {e}")
        return "Unknown Location"

# ✅ Function to generate AI-based reasoning
def generate_reason(origin_lat, origin_lon, dest_lat, dest_lon, distance):
    """Generate AI-based reasoning for the destination choice."""
    reason = f"This destination was selected because it is approximately {distance:.2f} km from the origin. "
    
    if distance < 50:
        reason += "The proximity suggests it is a nearby, frequently visited place."
    elif 50 <= distance < 200:
        reason += "The distance indicates a common regional travel destination."
    else:
        reason += "The location is farther away, possibly indicating an occasional travel or special visit."

    return reason

# ✅ Function to predict multiple destinations with reasoning
def predict_multiple_destinations_with_reason(model, scaler, user_id, df, n=3):
    """Predicts multiple destination locations for a given user with reasoning."""

    # Check for 'user_id' column
    if 'user_id' not in df.columns:
        print("❌ Error: 'user_id' column not found in the dataset.")
        return []

    user_data = df[df['user_id'] == user_id]

    if user_data.empty:
        print(f"❌ No data found for user ID {user_id}")
        return []

    user_features = user_data[features].values
    user_features_scaled = scaler.transform(user_features)

    predictions = model.predict(user_features_scaled)

    destinations = []
    for i, dest in enumerate(predictions[:n]):
        dest_lat, dest_lon = dest

        # ✅ Calculate distance between origin and predicted destination
        origin_lat, origin_lon = user_data.iloc[i]['Origin_Lat'], user_data.iloc[i]['Origin_Lon']
        distance = np.sqrt((origin_lat - dest_lat)**2 + (origin_lon - dest_lon)**2) * 111  # Approx km conversion

        location_name = get_location_name(dest_lat, dest_lon)
        reason = generate_reason(origin_lat, origin_lon, dest_lat, dest_lon, distance)

        destinations.append({
            "latitude": dest_lat,
            "longitude": dest_lon,
            "location_name": location_name,
            "reason": reason
        })

    return destinations

# ✅ Example usage
user_id = 1001
destinations = predict_multiple_destinations_with_reason(rf_model, scaler, user_id, df, n=3)

# ✅ Display predictions with reasoning
print("\n🔮 Predicted Destinations with Reasons:")
for i, dest in enumerate(destinations, 1):
    print(f"{i}. {dest['location_name']} (Lat: {dest['latitude']}, Lon: {dest['longitude']})")
    print(f"   💡 Reason: {dest['reason']}\n")
