import folium
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import json
import webbrowser
import os

# Load danger zones from JSON file
with open('danger_zones.json', 'r') as f:
    danger_zones = json.load(f)

def get_coordinates(location_name):
    geolocator = Nominatim(user_agent="danger-zone-locator")
    location = geolocator.geocode(location_name)
    if location:
        print(f"Coordinates of {location_name}: ({location.latitude}, {location.longitude})")
        return (location.latitude, location.longitude)
    else:
        print("Location not found!")
        return None

def find_nearby_danger_zones(user_coords, radius_km=5):
    nearby_zones = []
    for zone in danger_zones:
        zone_coords = tuple(zone["coordinates"])
        distance = geodesic(user_coords, zone_coords).km
        if distance <= radius_km:
            zone["distance_km"] = round(distance, 2)
            nearby_zones.append(zone)
    return nearby_zones

def create_map(user_coords, zones):
    my_map = folium.Map(location=user_coords, zoom_start=14)
    folium.Marker(user_coords, tooltip="You are here", icon=folium.Icon(color='blue')).add_to(my_map)

    for zone in zones:
        folium.Marker(
            location=zone["coordinates"],
            popup=f"{zone['name']} - {zone['danger_level']} Risk",
            icon=folium.Icon(color='red' if zone["danger_level"] == "High" else 'orange')
        ).add_to(my_map)

    map_filename = "danger_zones_map.html"
    my_map.save(map_filename)
    print("✅ Map saved as 'danger_zones_map.html'")

    # Automatically open the map in the browser
    webbrowser.open('file://' + os.path.realpath(map_filename))

if __name__ == "__main__":
    location_name = input("Enter your location (e.g., Bhubaneswar): ")
    coordinates = get_coordinates(location_name)

    if coordinates:
        zones = find_nearby_danger_zones(coordinates)

        if zones:
            print("\n🚨 Nearby Danger Zones (within 5 km):")
            for zone in zones:
                print(f"- {zone['name']} ({zone['danger_level']} risk) — {zone['distance_km']} km away")
            create_map(coordinates, zones)
        else:
            print("\n✅ No nearby danger zones found within 5 km.")
