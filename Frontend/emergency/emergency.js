// Service Worker Registration
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('service-worker.js')
        .then(() => console.log('Service Worker registered'))
        .catch((err) => console.error('Service Worker registration failed:', err));
    });
  }
  
  // Initialize map
  const map = L.map('map').setView([20.5937, 78.9629], 6); // Default to India
  
  const onlineLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
  }).addTo(map);
  
  let offlineLayer;
  
  // Switch Modes
  function goOnline() {
    map.addLayer(onlineLayer);
    if (offlineLayer) {
      map.removeLayer(offlineLayer);
    }
    showNotification('Online Mode', 'success');
  }
  
  function goOffline() {
    if (!offlineLayer) {
      offlineLayer = L.tileLayer('./tiles/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: 'Offline Cache'
      }).addTo(map);
    }
    map.removeLayer(onlineLayer);
    showNotification('Offline Mode', 'error');
  }
  
  // Notification
  function showNotification(message, type) {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.style.backgroundColor = type === 'error' ? '#e74c3c' : '#27ae60';
  
    setTimeout(() => {
      notification.textContent = '';
    }, 3000);
  }
  
  // Geolocation & Reverse Geocoding
  navigator.geolocation.getCurrentPosition(async (position) => {
    const { latitude, longitude } = position.coords;
    map.setView([latitude, longitude], 12);
  
    const area = await getAreaName(latitude, longitude);
    loadEmergencyServicesByArea(area);
  }, () => {
    console.error("Failed to get location");
  });
  
  async function getAreaName(lat, lng) {
    const url = `https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lng}&format=json`;
  
    try {
      const response = await fetch(url);
      const data = await response.json();
  
      const area = data.address.city || data.address.town || data.address.village || 'Unknown Area';
      console.log(`Detected Area: ${area}`);
      return area;
  
    } catch (error) {
      console.error('Failed to get area name:', error);
      return 'Unknown Area';
    }
  }
  
  // Load Emergency Services by Area
  async function loadEmergencyServicesByArea(area) {
    const servicesList = document.getElementById('services-list');
    servicesList.innerHTML = '<li>Loading...</li>';
  
    try {
      const response = await fetch('emergency.json');
      const services = await response.json();
      const filtered = services.filter(service => service.area === area);
  
      servicesList.innerHTML = '';
      if (filtered.length) {
        filtered.forEach(service => {
          const li = document.createElement('li');
          li.innerHTML = `<strong>${service.type}</strong>: ${service.name} - ${service.contact}`;
          servicesList.appendChild(li);
        });
      } else {
        servicesList.innerHTML = '<li>No services found for this area.</li>';
      }
    } catch (error) {
      console.error('Failed to load services:', error);
    }
  }
  
  // Search Filter
  function searchServices() {
    const searchInput = document.getElementById('searchInput').value.toLowerCase();
    const items = document.querySelectorAll('.emergency-container li');
  
    items.forEach((item) => {
      const text = item.textContent.toLowerCase();
      item.style.display = text.includes(searchInput) ? '' : 'none';
    });
  }
  
  // Clear Cache
  function clearCache() {
    caches.delete('emergency-cache-v1').then(() => {
      showNotification('Cache cleared successfully', 'success');
    });
  }
  