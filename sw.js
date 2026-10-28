/* Offline cache. Version comes from version.js (bump it there, nowhere else). */
importScripts("version.js");
const VERSION = self.APP_VERSION;
const CORE = ["./", "index.html", "styles.css", "app.js", "version.js", "manifest.webmanifest",
  "data/alefbet.json", "data/strokes.json", "icons/icon-192.png", "icons/icon-512.png"];
self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(VERSION).then((c) => c.addAll(CORE)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", (e) => {
  e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k !== VERSION).map((k) => caches.delete(k))))
    .then(() => self.clients.claim()));
});
// Own files: network first (updates arrive on the next open), cache as offline fallback.
// Fonts and other sites: cache first. Anything fetched (data, audio) is kept for offline use.
self.addEventListener("fetch", (e) => {
  if (e.request.method !== "GET") return;
  const own = new URL(e.request.url).origin === location.origin;
  e.respondWith(caches.open(VERSION).then(async (c) => {
    const hit = await c.match(e.request, { ignoreSearch: true });
    // no-cache: always ask GitHub whether the file changed (its HTTP cache otherwise serves old files for ~10 min)
    const net = () => fetch(own ? new Request(e.request.url, { cache: "no-cache", credentials: "same-origin" }) : e.request).then((r) => { if (r && (r.ok || r.type === "opaque")) c.put(e.request, r.clone()); return r; });
    if (own) return net().catch(() => hit || Response.error());
    return hit || net().catch(() => Response.error());
  }));
});
