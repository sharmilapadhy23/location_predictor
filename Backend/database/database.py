import os
import csv

def extract_gps_data(file_path):
    """Extract latitude, longitude, and timestamp from a single .plt file."""
    gps_data = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            
            # ✅ Skip headers (first 6 lines) and process first 100 rows only
            for i, line in enumerate(lines[6:106]):  
                data = line.strip().split(",")

                latitude = data[0].strip()
                longitude = data[1].strip()
                timestamp = data[5].strip() + " " + data[6].strip()  # Date + Time
                
                gps_data.append([latitude, longitude, timestamp])

    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
    except Exception as e:
        print(f"❌ Error reading GPS data from {file_path}: {e}")

    return gps_data

def extract_and_save_gps_data(dataset_folder, output_csv):
    """Extract GPS data from all users and save it into a structured CSV file."""
    all_data = []

    for user_folder in os.listdir(dataset_folder):  
        print(f"📌 Processing user: {user_folder}...")  # ✅ Show progress
        trajectory_path = os.path.join(dataset_folder, user_folder, "Trajectory")
        
        if os.path.exists(trajectory_path):  
            files = os.listdir(trajectory_path)[:5]  # ✅ Limit to first 5 files

            for file in files:
                file_path = os.path.join(trajectory_path, file)
                print(f"   ✅ Processing file: {file}")  # ✅ Show file name
                gps_points = extract_gps_data(file_path)
                
                for point in gps_points:
                    # ✅ Add user ID (folder name) to each row
                    all_data.append([000] + point)  

    try:
        with open(output_csv, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["user_id", "latitude", "longitude", "timestamp"])  # ✅ Headers
            writer.writerows(all_data)
        print(f"✅ Processed data saved to {output_csv}")
    except Exception as e:
        print(f"❌ Error saving CSV: {e}")

# ✅ Run the extraction process
dataset_path = "../data/Geolife Trajectories 1.3/Data"
output_csv = "../data/processed_data.csv"
extract_and_save_gps_data(dataset_path, output_csv)
