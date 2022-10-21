var staticCacheName = "django-pwa-v" + new Date().getTime();
var filesToCache = [
    '/',
    '/static/css/layout.css',
    '/static/images/Ferme-nav.png',
    '/static/css/agregar_productos.css',
    '/static/css/editar_cliente.css',
    '/static/css/editar_perfil.css',
    '/static/css/index.css',
    '/static/css/ingreso_usuarios.css',
    '/static/css/modulo_pedidos.css',
    '/static/css/modulo_productos.css',
    '/static/css/modulo_proveedores.css',
    '/static/css/recepcion_productos.css',
    '/static/css/registro_clientes_emp.css',
    '/static/css/registro_clientes.css',
    '/static/css/seleccion_registro.css',
];

self.addEventListener("install", event => {
    this.skipWaiting();
    event.waitUntil(
        caches.open(staticCacheName)
            .then(cache => {
                return cache.addAll(filesToCache);
            })
    )
});

self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames
                    .filter(cacheName => (cacheName.startsWith("django-pwa-")))
                    .filter(cacheName => (cacheName !== staticCacheName))
                    .map(cacheName => caches.delete(cacheName))
            );
        })
    );
});

// self.addEventListener("fetch", event => {
//     event.respondWith(
//         caches.match(event.request)
//             .then(response => {
//                 return response || fetch(event.request);
//             })
//             .catch(() => {
//                 return caches.match('/offline/');
//             })
//     )
// });

self.addEventListener("fetch", function(event) {
    event.respondWith(
        fetch(event.request)
        .then(function(result) {
            return caches.open(staticCacheName)
            .then(function(c) {
                c.put(event.request.url, result.clone())
                return result;
            })
        })
        .catch(function(e){
            return caches.match(event.request);
        })
    )
});