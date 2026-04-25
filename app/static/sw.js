const CACHE_NAME = "anxingban-ui-v36";
const ASSETS = [
  "/",
  "/static/index.html",
  "/static/styles.css",
  "/static/app.js",
  "/static/manifest.webmanifest",
  "/static/tropical-bg.svg",
  "/static/cover-photo.jpg",
  "/static/poster/hongyadong.jpg",
  "/static/poster/ciqikou.jpg",
  "/static/poster/wulong.jpg",
  "/static/poster/changjiangsuodao.jpg",
  "/static/poster/background.png",
];

self.addEventListener("install", (event) => {
  self.skipWaiting();
  event.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS)));
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k))))
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;
  event.respondWith(
    fetch(event.request).catch(() => caches.match(event.request).then((res) => res || caches.match("/")))
  );
});
