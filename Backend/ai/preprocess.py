import csv
import datetime

# File paths
input_file = "../data/Geolife Trajectories 1.3/Data/000/Trajectory/20081023025304.plt"
output_file = "../data/processed_data.csv"

def convert_excel_date(excel_date):
    """Convert Excel serial date to standard datetime format."""
    base_date = datetime.datetime(1899, 12, 30)
    return base_date + datetime.timedelta(days=float(excel_date))

# Process the file
processed_data = []

with open(input_file, "r") as file:
    lines = file.readlines()
    
    for line in lines[6:]:  # Skip metadata
        parts = line.strip().split(',')
        if len(parts) < 7:
            continue  # Skip malformed lines
        
        lat, lon, _, alt, excel_date, date_str, time_str = parts[:7]

        try:
            timestamp = convert_excel_date(excel_date)  # Convert Excel serial date
            processed_data.append([float(lat), float(lon), int(alt), timestamp])
        except ValueError:
            continue  # Skip invalid entries

# Save processed data to CSV
with open(output_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Latitude", "Longitude", "Altitude (ft)", "Timestamp"])
    writer.writerows(processed_data)

print(f"✅ Processed data saved to {output_file}")
