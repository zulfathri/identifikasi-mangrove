// Service worker: menyimpan aplikasi agar bisa dibuka tanpa sinyal.
// Naikkan VERSI setiap kali index.html, ikon, atau berkas lain (selain data) diubah.
const VERSI = 'kunci-mangrove-v1';
const INTI = ['./', 'index.html', 'data/mangrove.json', 'manifest.webmanifest',
  'icons/icon-192.png', 'icons/icon-512.png', 'icons/icon-maskable-512.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(VERSI).then(c => c.addAll(INTI)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== VERSI).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET') return;
  // Halaman & data: ambil versi terbaru bila ada sinyal, pakai simpanan bila tidak.
  if (url.origin === location.origin && (e.request.mode === 'navigate' || url.pathname.endsWith('.json'))) {
    e.respondWith(fetch(e.request).then(r => { const c = r.clone(); caches.open(VERSI).then(x => x.put(e.request, c)); return r; })
      .catch(() => caches.match(e.request).then(r => r || caches.match('index.html'))));
    return;
  }
  // Huruf Google Fonts & berkas lain: pakai simpanan dulu.
  if (url.origin === location.origin || /fonts\.(googleapis|gstatic)\.com$/.test(url.hostname)) {
    e.respondWith(caches.match(e.request).then(r => r || fetch(e.request).then(res => {
      const c = res.clone(); caches.open(VERSI).then(x => x.put(e.request, c)); return res; })));
  }
});
