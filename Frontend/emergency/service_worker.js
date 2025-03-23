const CACHE_NAME = 'emergency-cache-v1';
const urlsToCache = [
  '/',
  '/emergency.html',
  '/emergency.css',
  '/emergency.js',
  './data/emergency.json',
  '/manifest.json'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => response || fetch(event.request))
  );
});
