import pandas as pd
import joblib
import numpy as np
from collections import Counter
import requests

# ✅ File Paths
MODEL_FILE = r'C:\Users\KIIT\Desktop\project\Location_Predictor\Backend\models\location_model.pkl'
ENCODER_FILE = r'C:\Users\KIIT\Desktop\project\Location_Predictor\Backend\models\encoder.pkl'
PROCESSED_CSV_FILE = r'C:\Users\KIIT\Desktop\project\Location_Predictor\Backend\data\processed_travel_history.csv'

# ✅ Weather API Configuration
WEATHER_API_KEY = "df9bef60ab0bab2ec570b05a568d5067"  # Replace with your API key
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

# ✅ Step 1: Load the Model, Encoder, and Data
def load_assets():
    """Load model, encoder, and travel history data."""
    print("🔹 Loading model, encoder, and data...")
    model = joblib.load(MODEL_FILE)
    encoder = joblib.load(ENCODER_FILE)
    data = pd.read_csv(PROCESSED_CSV_FILE)
    print("✅ Assets loaded successfully!")
    return model, encoder, data


# ✅ Step 2: Prepare Input Data for Prediction
def prepare_input():
    """Create sample input data."""
    new_data = pd.DataFrame({
        'start_city': ['Shimla'],
        'start_state': ['Himachal Pradesh'],
        'start_country': ['India'],
        'end_city': ['Bhopal'],
        'end_state': ['Madhya Pradesh'],
        'end_country': ['India'],
        'distance_km': [296],
        'mode_of_transport': ['Car'],
        'purpose': ['Family Visit']
    })
    return new_data


# ✅ Step 3: Encode Input Data
def encode_input(encoder, new_data):
    """Encode input data."""
    print("🔥 Encoding input data...")
    X_new_encoded = encoder.transform(new_data)
    return X_new_encoded


# ✅ Step 4: Make Prediction
def predict_destination(model, X_new_encoded):
    """Predict the user ID based on input data."""
    print("🚀 Making prediction...")
    predicted_user_id = model.predict(X_new_encoded)[0]
    print(f"✅ Predicted user_id: {predicted_user_id}")
    return predicted_user_id


# ✅ Step 5: Recommend Next Location
def recommend_location(user_id, data):
    """Recommend the next location based on the user's past travel history."""
    print("🔍 Recommending next location based on past experiences...")
    
    user_history = data[data['user_id'] == user_id]

    if not user_history.empty:
        next_destinations = user_history[['end_city', 'end_state', 'end_country']].values.tolist()

        # Count occurrences
        destination_counter = Counter(map(tuple, next_destinations))
        most_common_destination, freq = destination_counter.most_common(1)[0]

        print("\n✅ Recommended Next Location Based on Past Experiences:")
        print(f"🌍 City: {most_common_destination[0]}")
        print(f"🏙️ State: {most_common_destination[1]}")
        print(f"🌏 Country: {most_common_destination[2]}")
        print(f"📊 Frequency: {freq} occurrences")
        return most_common_destination
    else:
        print("❌ No past travel data found for this user.")
        return None


# ✅ Step 6: Fetch Weather Information
def get_weather(city, country):
    """Fetch current weather data for a location."""
    params = {
        "q": f"{city},{country}",
        "appid": WEATHER_API_KEY,
        "units": "metric"
    }
    try:
        response = requests.get(WEATHER_URL, params=params)
        weather_data = response.json()

        if response.status_code == 200:
            temp = weather_data['main']['temp']
            condition = weather_data['weather'][0]['description']
            return temp, condition
        else:
            return None, None
    except Exception as e:
        print(f"❌ Error fetching weather data: {e}")
        return None, None


# ✅ Step 7: Suggest New Destinations
def suggest_new_destinations(user_id, data):
    """Suggest new destinations based on similar users' travel patterns."""
    print("\n✨ Suggesting new destinations based on similar users...")

    # Find similar users
    similar_users = data[data['user_id'] != user_id]

    # Get destinations user hasn't visited
    user_history = data[data['user_id'] == user_id]
    visited_places = set(user_history['end_city'].tolist())

    new_places = similar_users[~similar_users['end_city'].isin(visited_places)][['end_city', 'end_state', 'end_country']]

    if not new_places.empty:
        suggestions = new_places.sample(n=min(3, len(new_places)), replace=False).values.tolist()

        print("\n🌟 New Destination Suggestions:")
        for i, (city, state, country) in enumerate(suggestions, 1):
            print(f"{i}. 🌍 {city}, {state}, {country}")
    else:
        print("❌ No new locations found to recommend.")


# ✅ Main Execution
def main():
    # Load assets
    model, encoder, data = load_assets()

    # Prepare and encode input
    new_data = prepare_input()
    X_new_encoded = encode_input(encoder, new_data)

    # Predict and recommend
    predicted_user_id = predict_destination(model, X_new_encoded)
    most_common_destination = recommend_location(predicted_user_id, data)

    # Fetch and display weather info
    if most_common_destination:
        city, state, country = most_common_destination
        temp, condition = get_weather(city, country)

        if temp and condition:
            print(f"\n🌤️ Weather in {city}, {country}:")
            print(f"🌡️ Temperature: {temp}°C")
            print(f"☁️ Condition: {condition}")

            # Weather-based suggestions
            if temp > 30:
                print("🥵 It's quite hot there! You might prefer a cooler destination.")
            elif temp < 10:
                print("❄️ It's cold! Pack warm clothes.")
            else:
                print("🌿 The weather is pleasant. Enjoy your trip!")

        # Suggest new destinations
        suggest_new_destinations(predicted_user_id, data)

    else:
        print("❌ Unable to recommend next location.")

# Run the program
if __name__ == "__main__":
    main()
