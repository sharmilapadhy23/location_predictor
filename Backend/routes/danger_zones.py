from flask import Blueprint, jsonify, request
import pandas as pd
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Create blueprint
danger_zones_blueprint = Blueprint('danger_zones', __name__)

# File paths
CSV_FILE_PATH = os.path.join(os.path.dirname(__file__), '../data/danger_zones.csv')
MODELS_FOLDER = os.path.join(os.path.dirname(__file__), '../models')
MODEL_PATH = os.path.join(MODELS_FOLDER, 'danger_zone_model.pkl')

# Ensure the models folder exists
if not os.path.exists(MODELS_FOLDER):
    os.makedirs(MODELS_FOLDER)
    print(f"📁 Created models folder: {MODELS_FOLDER}")

# ✅ Function to train and save the model
def train_and_save_model():
    """Train the model using zone and state and save it as a pickle file."""
    try:
        print("📊 Loading CSV for training...")
        df = pd.read_csv(CSV_FILE_PATH)

        if df.empty:
            print("⚠️ CSV file is empty. No model will be created.")
            return

        # Extract features (zone, state) and labels (risk_level)
        X = df[['zone', 'state']]  # Using zone and state as features
        y = df['risk_level']

        # Encode labels
        encoder = LabelEncoder()
        y_encoded = encoder.fit_transform(y)

        # Encode categorical features (zone and state)
        zone_encoder = LabelEncoder()
        state_encoder = LabelEncoder()
        X['zone_encoded'] = zone_encoder.fit_transform(X['zone'])
        X['state_encoded'] = state_encoder.fit_transform(X['state'])

        # Use the encoded columns as features
        X_encoded = X[['zone_encoded', 'state_encoded']]

        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(X_encoded, y_encoded, test_size=0.2, random_state=42)

        # Train the model
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Save the model
        joblib.dump(model, MODEL_PATH)
        print(f"✅ Model trained and saved at: {MODEL_PATH}")

    except Exception as e:
        print(f"❌ Error training the model: {e}")

# ✅ Function to load the model
def load_model():
    """Load the model if it exists; otherwise, train a new one."""
    try:
        if os.path.exists(MODEL_PATH):
            model = joblib.load(MODEL_PATH)
            print("✅ Model loaded successfully.")
        else:
            print("⚠️ Model not found. Training a new model...")
            train_and_save_model()
            model = joblib.load(MODEL_PATH)

        return model

    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return None

# ✅ Function to load danger zones and predict risk levels based on zone and state
def load_and_predict_danger_zones():
    """Load danger zones from CSV and predict risk levels using the ML model."""
    try:
        print("📊 Loading CSV for predictions...")
        df = pd.read_csv(CSV_FILE_PATH)

        if df.empty:
            print("⚠️ No data found in CSV.")
            return []

        # Prepare features (zone, state)
        features = df[['zone', 'state']]

        # Encode the features
        zone_encoder = LabelEncoder()
        state_encoder = LabelEncoder()
        features['zone_encoded'] = zone_encoder.fit_transform(features['zone'])
        features['state_encoded'] = state_encoder.fit_transform(features['state'])

        features_encoded = features[['zone_encoded', 'state_encoded']]

        # Load the model
        model = load_model()

        if model:
            print("🔍 Making predictions...")
            predictions = model.predict(features_encoded)
            df['Predicted Risk Level'] = predictions
        else:
            print("⚠️ No model available, assigning 'Unknown' risk level.")
            df['Predicted Risk Level'] = 'Unknown'

        # Convert to dictionary
        danger_zones = df.to_dict(orient='records')
        return danger_zones

    except Exception as e:
        print(f"❌ Error loading or predicting: {e}")
        return []

# ✅ Endpoint to get predicted danger zones
@danger_zones_blueprint.route('/', methods=['GET'])
def get_danger_zones():
    """API endpoint to fetch all danger zones with predicted risk levels."""
    print("🚀 Fetching danger zones...")

    danger_zones = load_and_predict_danger_zones()

    if danger_zones:
        return jsonify(danger_zones)
    else:
        return jsonify({"error": "No danger zones found or failed to load CSV."}), 500


# ✅ Main execution block to test locally
if __name__ == "__main__":
    try:
        print("🚀 Running danger_zones.py script...")
        # Test model generation and predictions
        danger_zones = load_and_predict_danger_zones()
        print("✅ Sample Danger Zones with Predictions:")
        for zone in danger_zones[:5]:
            print(zone)

    except Exception as e:
        print(f"❌ Error: {e}")
