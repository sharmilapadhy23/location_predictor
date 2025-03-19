import pandas as pd
import os

# ✅ File Paths
RAW_CSV_FILE = r'C:\Users\KIIT\Desktop\project\Location_Predictor\Backend\data\large_travel_history.csv'
PROCESSED_CSV_FILE = r'C:\Users\KIIT\Desktop\project\Location_Predictor\Backend\data\processed_travel_history.csv'

# ✅ Step 1: Load Dataset
print("🔹 Loading raw dataset...")

if not os.path.exists(RAW_CSV_FILE):
    print(f"❌ CSV file not found: {RAW_CSV_FILE}")
    exit()

data = pd.read_csv(RAW_CSV_FILE)
print(f"✅ Data loaded successfully. Shape: {data.shape}")

# ✅ Step 2: Validate Columns
EXPECTED_COLUMNS = {
    'user_id', 'timestamp', 'start_city', 'start_state', 'start_country',
    'end_city', 'end_state', 'end_country', 'distance_km', 'mode_of_transport', 'purpose'
}

# Detect missing columns
missing_cols = EXPECTED_COLUMNS - set(data.columns)

if missing_cols:
    print(f"⚠️ Missing columns: {missing_cols}")
    exit()
else:
    print("✅ All columns are present!")

# ✅ Step 3: Handle Missing Values
print("🔧 Handling missing values...")

# Fill missing city/state/country with "Unknown"
data['start_city'].fillna('Unknown', inplace=True)
data['start_state'].fillna('Unknown', inplace=True)
data['start_country'].fillna('Unknown', inplace=True)
data['end_city'].fillna('Unknown', inplace=True)
data['end_state'].fillna('Unknown', inplace=True)
data['end_country'].fillna('Unknown', inplace=True)

# Fill missing distance with 0 and transport/purpose with "Unknown"
data['distance_km'].fillna(0.0, inplace=True)
data['mode_of_transport'].fillna('Unknown', inplace=True)
data['purpose'].fillna('Unknown', inplace=True)

print("✅ Missing values handled!")

# ✅ Step 4: Remove Duplicates
print("🧹 Removing duplicates...")
before_dedup = data.shape[0]
data.drop_duplicates(inplace=True)
after_dedup = data.shape[0]
print(f"✅ Removed {before_dedup - after_dedup} duplicate rows!")

# ✅ Step 5: Save the Cleaned Data
print(f"💾 Saving cleaned data to: {PROCESSED_CSV_FILE}")
data.to_csv(PROCESSED_CSV_FILE, index=False)
print("✅ Preprocessing completed successfully!")
