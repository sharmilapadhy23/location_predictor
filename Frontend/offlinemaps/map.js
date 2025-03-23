if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('service-worker.js')
        .then(() => console.log('Service Worker registered'))
        .catch((err) => console.error('Service Worker registration failed:', err));
    });
  }
  
  const map = L.map('map').setView([20.5937, 78.9629], 5); // Center on India
  
  // Online tiles
  const onlineLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18
  }).addTo(map);
  
  let offlineLayer;
  const tileCache = {};  // Local cache to store fetched tiles
  
  // Switch to online mode
  function goOnline() {
    map.addLayer(onlineLayer);
    if (offlineLayer) {
      map.removeLayer(offlineLayer);
    }
    console.log("Switched to online mode");
  }
  
  // Switch to offline mode
  function goOffline() {
    if (!offlineLayer) {
      offlineLayer = L.tileLayer('./tiles/{z}/{x}/{y}.png', {
        maxZoom: 18
      }).addTo(map);
    }
    map.removeLayer(onlineLayer);
    console.log("Switched to offline mode");
  }
  
  // Cache tiles when online
  map.on('moveend', async () => {
    if (navigator.onLine) {
      const bounds = map.getBounds();
      const zoom = map.getZoom();
      
      const tileSize = 256;
      const minX = Math.floor(bounds.getWest() * tileSize);
      const maxX = Math.ceil(bounds.getEast() * tileSize);
      const minY = Math.floor(bounds.getSouth() * tileSize);
      const maxY = Math.ceil(bounds.getNorth() * tileSize);
  
      for (let x = minX; x <= maxX; x += tileSize) {
        for (let y = minY; y <= maxY; y += tileSize) {
          const tileUrl = `https://tile.openstreetmap.org/${zoom}/${x}/${y}.png`;
  
          // Avoid duplicate caching
          if (!tileCache[tileUrl]) {
            try {
              const response = await fetch(tileUrl);
              if (response.ok) {
                const blob = await response.blob();
                saveTileToDB(tileUrl, blob);   // Save to IndexedDB
                tileCache[tileUrl] = true;    // Mark tile as cached
                console.log(`Cached tile: ${tileUrl}`);
              }
            } catch (error) {
              console.error(`Failed to cache tile: ${tileUrl}`, error);
            }
          }
        }
      }
    }
  });
  
  // Save tile to IndexedDB
  async function saveTileToDB(url, blob) {
    const db = await openDB();
    const tx = db.transaction('tiles', 'readwrite');
    const store = tx.objectStore('tiles');
  
    await store.put(blob, url);
    await tx.complete;
    console.log(`Tile saved to DB: ${url}`);
  }
  
  // Open IndexedDB
  function openDB() {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open('mapTilesDB', 1);
  
      request.onupgradeneeded = (event) => {
        const db = event.target.result;
        if (!db.objectStoreNames.contains('tiles')) {
          db.createObjectStore('tiles');
        }
      };
  
      request.onsuccess = (event) => {
        resolve(event.target.result);
      };
  
      request.onerror = (event) => {
        reject(`IndexedDB error: ${event.target.errorCode}`);
      };
    });
  }
  