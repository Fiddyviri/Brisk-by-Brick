if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/static/service-worker.js')
        .then(function(registration) {
            console.log("Service Worker registered:", registration);
        })
        .catch(function(error) {
            console.log("Service Worker registration failed:", error);
        });
    });
}
