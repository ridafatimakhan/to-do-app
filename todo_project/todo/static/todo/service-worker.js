const CACHE_NAME = 'todo-app-cache-v1';
const urlsToCache = [
    '/', // home page
    '/task-list', // add other essential URLs here
    '/add-task', // add other URLs like Add Task page
    '/static/', // Cache static resources
    '/styles.css',
    '/scripts.js',
    // Add other URLs for caching, e.g., images, etc.
];

// Installing the service worker and caching the resources
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('Caching essential resources...');
                return cache.addAll(urlsToCache);
            })
    );
});

// Activate the service worker and clean up old caches
self.addEventListener('activate', (event) => {
    const cacheWhitelist = [CACHE_NAME];
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (!cacheWhitelist.includes(cacheName)) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});

// Fetch data from cache or fetch it from the network when online
self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request)
            .then((cachedResponse) => {
                // Return cached response if available
                if (cachedResponse) {
                    return cachedResponse;
                }
                // Otherwise, fetch from the network
                return fetch(event.request);
            })
    );
});
