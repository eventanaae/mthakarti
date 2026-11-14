/* Mthakarti service worker: shows the daily 4:30 PM study reminder sent by the server */
self.addEventListener('install', function () { self.skipWaiting(); });
self.addEventListener('activate', function (e) { e.waitUntil(self.clients.claim()); });
self.addEventListener('push', function (e) {
  var d = {};
  try { d = e.data ? e.data.json() : {}; } catch (x) { d = { body: e.data ? e.data.text() : '' }; }
  var title = d.title || 'مذاكرتي 📚';
  e.waitUntil(self.registration.showNotification(title, {
    body: d.body || 'يالله، وقت المذاكرة! 📚',
    icon: '/icon-192.png',
    badge: '/icon-192.png',
    tag: 'mthakarti-daily',
    renotify: true,
    data: { url: d.url || 'https://mthakarti.com/#home' }
  }));
});
self.addEventListener('notificationclick', function (e) {
  e.notification.close();
  var url = (e.notification.data && e.notification.data.url) || '/';
  e.waitUntil(self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then(function (list) {
    for (var i = 0; i < list.length; i++) { if ('focus' in list[i]) { list[i].navigate(url); return list[i].focus(); } }
    return self.clients.openWindow(url);
  }));
});
