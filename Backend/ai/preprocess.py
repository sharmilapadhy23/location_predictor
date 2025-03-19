import os
import csv
import requests
import time

# OpenCage API Key (Replace with your actual key)
API_KEY = '97affb5510db483e88242f4d48f3d3e1'

# Use absolute paths for file locations
INPUT_CSV = r'C:\Users\KIIT\Desktop\project\Location_Predictor\Backend\data\large_travel_history.csv'  
OUTPUT_CSV = r'C:\Users\KIIT\Desktop\project\Location_Predictor\Backend\data\processed_travel_history.csv'

# Function to get latitude and longitude using OpenCage API
def get_lat_lon(city, state, country):
    """Get latitude and longitude for a given location."""
    try:
        location = f"{city}, {state}, {country}"
        url = f"https://api.opencagedata.com/geocode/v1/json?q={location}&key={API_KEY}"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200 and data['results']:
            lat = data['results'][0]['geometry']['lat']
            lon = data['results'][0]['geometry']['lng']
            return lat, lon
        else:
            print(f"⚠️ No data found for {location}.")
            return None, None
    except Exception as e:
        print(f"❌ Error fetching location data: {e}")
        return None, None

# Function to preprocess CSV
def preprocess_csv(input_file, output_file):
    """Preprocess CSV file by adding latitude and longitude."""
    
    # Check if the input file exists
    if not os.path.exists(input_file):
        print(f"❌ Input file not found: {input_file}")
        return

    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Read headers and add new latitude/longitude columns
        headers = next(reader)
        headers.extend(['Origin_Lat', 'Origin_Lon', 'Dest_Lat', 'Dest_Lon'])
        writer.writerow(headers)

        for row in reader:
            try:
                origin_city = row[2]
                origin_state = row[3]
                origin_country = row[4]
                dest_city = row[5]
                dest_state = row[6]
                dest_country = row[7]

                # Get lat/lon for origin and destination
                origin_lat, origin_lon = get_lat_lon(origin_city, origin_state, origin_country)
                dest_lat, dest_lon = get_lat_lon(dest_city, dest_state, dest_country)

                if origin_lat is None or dest_lat is None:
                    print(f"⚠️ Skipping row due to missing coordinates: {row}")
                    continue

                # Add lat/lon to the row
                row.extend([origin_lat, origin_lon, dest_lat, dest_lon])
                writer.writerow(row)

                print(f"✅ Processed: {origin_city} ➡️ {dest_city}")
                time.sleep(1)  # Prevent API rate limit issues

            except Exception as e:
                print(f"❌ Error processing row: {row} - {e}")

# Run preprocessing
if __name__ == "__main__":
    print(f"📊 Preprocessing CSV: {INPUT_CSV}")
    preprocess_csv(INPUT_CSV, OUTPUT_CSV)
    print(f"✅ Processed data saved at: {OUTPUT_CSV}")
