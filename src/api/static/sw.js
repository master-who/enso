// Service Worker
const CACHE_NAME = 'enso-v1';
const CACHE_VERSION = 'v1.1';
const urlsToCache = [
  '/',
  '/static/styles.css',
  '/manifest.json'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});

self.addEventListener('push', event => {
  const options = {
    body: event.data.text(),
    icon: '/static/icon-192x192.png',
    badge: '/static/icon-192x192.png'
  };

  event.waitUntil(
    self.registration.showNotification('Enso', options)
  );
});
