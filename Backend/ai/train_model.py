import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
import joblib

# ✅ File Paths
PROCESSED_CSV_FILE = r'C:\Users\KIIT\Desktop\project\Location_Predictor\Backend\data\processed_travel_history.csv'
MODEL_FILE = r'C:\Users\KIIT\Desktop\project\Location_Predictor\Backend\models\location_model.pkl'

# ✅ Step 1: Load Processed Data
print("🔹 Loading cleaned dataset...")
data = pd.read_csv(PROCESSED_CSV_FILE)
print(f"✅ Data loaded. Shape: {data.shape}")

# ✅ Step 2: Prepare Features and Labels
X = data[['start_city', 'start_state', 'start_country', 
          'end_city', 'end_state', 'end_country', 
          'distance_km', 'mode_of_transport', 'purpose']]

y = data['user_id']  # Assuming the goal is to predict user_id for now

# ✅ Step 3: One-Hot Encoding for Categorical Variables
print("🔥 Encoding categorical features...")
encoder = OneHotEncoder(handle_unknown='ignore')
X_encoded = encoder.fit_transform(X)

# ✅ Step 4: Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

# ✅ Step 5: Train the Model
print("🚀 Training model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
print("✅ Model training completed!")

# ✅ Step 6: Save the Model and Encoder
print(f"💾 Saving model to: {MODEL_FILE}")
joblib.dump(model, MODEL_FILE)
joblib.dump(encoder, r'C:\Users\KIIT\Desktop\project\Location_Predictor\Backend\models\encoder.pkl')
print("✅ Model saved successfully!")
