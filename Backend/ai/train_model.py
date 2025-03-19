import pandas as pd
import os
import joblib  # For saving and loading the trained model
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler

# ✅ File paths
csv_file = r"C:\Users\KIIT\Desktop\project\Location_Predictor\Backend\data\processed_travel_history.csv"
models_folder = r"C:\Users\KIIT\Desktop\project\Location_Predictor\Backend\models"

# ✅ Ensure the models folder exists
if not os.path.exists(models_folder):
    os.makedirs(models_folder)
    print(f"📁 Created models folder at {models_folder}")

model_file = os.path.join(models_folder, "travel_model.pkl")
scaler_file = os.path.join(models_folder, "scaler.pkl")

# 🔥 Verify the file exists before reading
if not os.path.exists(csv_file):
    print(f"❌ Error: File not found at {csv_file}")
    exit()

# ✅ Load dataset
df = pd.read_csv(csv_file)

# ✅ Train the model
def train_model(df, model_file, scaler_file):
    """Trains the RandomForest model and saves it along with the scaler."""
    
    features = ['Origin_Lat', 'Origin_Lon', 'distance_km']
    target = ['Dest_Lat', 'Dest_Lon']

    X = df[features]
    y = df[target]

    # ✅ Scale the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # ✅ Train RandomForestRegressor
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_scaled, y)

    # ✅ Save model and scaler
    joblib.dump(rf_model, model_file)
    joblib.dump(scaler, scaler_file)

    print(f"✅ Model and scaler saved successfully at {model_file} and {scaler_file}.")

# ✅ Execute training
if __name__ == "__main__":
    print("🚀 Training the model...")
    train_model(df, model_file, scaler_file)
    print("🎯 Training completed successfully!")
