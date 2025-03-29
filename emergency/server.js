// Fetch nearest emergency service using ML predictions
async function findNearestEmergency(lat, lng) {
    try {
        const response = await fetch('http://localhost:3000/nearest', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ lat, lon: lng })
        });

        const data = await response.json();

        // Display the nearest emergency service with ETA prediction
        const { nearest } = data;
        console.log("Nearest Service:", nearest);

        const marker = L.marker([nearest.lat, nearest.lon])
            .addTo(map)
            .bindPopup(`
                <strong>${nearest.type.toUpperCase()}</strong><br>
                Distance: ${(nearest.distance / 1000).toFixed(2)} km<br>
                ETA (ML Prediction): ${nearest.eta} mins
            `)
            .openPopup();

        map.setView([nearest.lat, nearest.lon], 14);

    } catch (error) {
        console.error("Error fetching nearest service:", error);
    }
}

// Initialize map and geolocation
navigator.geolocation.getCurrentPosition((position) => {
    const { latitude, longitude } = position.coords;
    
    map.setView([latitude, longitude], 14);
    
    L.marker([latitude, longitude])
        .addTo(map)
        .bindPopup("You are here")
        .openPopup();

    // Find nearest service with ML predictions
    findNearestEmergency(latitude, longitude);

}, () => {
    alert("Failed to detect your location.");
});
