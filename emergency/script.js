// Initialize the map
let map = L.map('map').setView([28.7041, 77.1025], 14);  // Default to Delhi

// Load and display map tiles from OpenStreetMap
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
}).addTo(map);

let userMarker, serviceMarkers = [];

// Get User's current location and enable "Find Nearby"
navigator.geolocation.getCurrentPosition((position) => {
    const { latitude, longitude } = position.coords;

    // Set map view to user's location
    map.setView([latitude, longitude], 14);

    userMarker = L.marker([latitude, longitude])
        .addTo(map)
        .bindPopup("You are here")
        .openPopup();

    // Find all nearby emergency services
    setTimeout(() => {
        findNearbyEmergency(latitude, longitude);
    }, 500);

}, () => {
    alert("Failed to detect your location.");
});

// Function to find nearby emergency services using Overpass API
function findNearbyEmergency(lat, lng) {
    const radius = 3000;  // 3 km radius
    const emergencyTypes = [
        "hospital", "police", "fire_station", "pharmacy",  // Medicine shops included here
        "emergency", "ambulance_station", "rescue_station",
        "healthcare", "clinic", "doctors", "nursing_home",
        "office=police", "emergency=service", "fuel"  // Added fuel stations
    ];

    serviceMarkers.forEach(marker => map.removeLayer(marker));
    serviceMarkers = [];

    emergencyTypes.forEach(type => {
        const query = `
            [out:json];
            (
                node["amenity"="${type}"](around:${radius},${lat},${lng});
                way["amenity"="${type}"](around:${radius},${lat},${lng});
                relation["amenity"="${type}"](around:${radius},${lat},${lng});
            );
            out center;
        `;

        const url = `https://overpass-api.de/api/interpreter?data=${encodeURIComponent(query)}`;
        
        fetchDataWithRetry(url, 3);
    });
}

// Fetch function with retry logic
function fetchDataWithRetry(url, retries) {
    fetch(url)
        .then((response) => response.json())
        .then((data) => {
            console.log("Fetched data:", data);

            if (data.elements.length === 0) {
                console.log("No emergency services found for this query.");
                return;
            }

            // Display emergency services on the map
            data.elements.forEach((place) => {
                const lat = place.lat || place.center?.lat;
                const lon = place.lon || place.center?.lon;
                const type = place.tags.amenity || place.tags.office || place.tags.emergency || "Unknown";

                if (lat && lon) {
                    const marker = L.marker([lat, lon])
                        .addTo(map)
                        .bindPopup(`
                            <strong>${type.toUpperCase()}</strong><br>
                            ${place.tags.name || "Unnamed"}<br>
                            Lat: ${lat}<br>
                            Lon: ${lon}
                        `);

                    serviceMarkers.push(marker);
                }
            });

            // Fit map bounds to include all markers
            if (serviceMarkers.length > 0) {
                const bounds = L.latLngBounds(serviceMarkers.map(marker => marker.getLatLng()));
                bounds.extend(userMarker.getLatLng());
                map.fitBounds(bounds);
            }
        })
        .catch((error) => {
            console.error("Error fetching emergency services:", error);

            if (retries > 0) {
                console.log(`Retrying... (${retries} attempts left)`);
                fetchDataWithRetry(url, retries - 1);
            } else {
                alert("Failed to load emergency services after multiple attempts.");
            }
        });
}

// SOS Functionality
function sendSOS() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition((position) => {
            const lat = position.coords.latitude;
            const lng = position.coords.longitude;

            const message = `🚨 SOS Alert! 
            Location: https://www.openstreetmap.org/?mlat=${lat}&mlon=${lng}`;

            alert(`SOS sent to your emergency contact!\n${message}`);

            console.log("Sending SOS message: ", message);
        });
    } else {
        alert("Geolocation not supported by this browser.");
    }
}