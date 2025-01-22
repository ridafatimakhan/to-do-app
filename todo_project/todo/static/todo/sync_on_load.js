// Sync tasks when the page is loaded and the user is online
window.addEventListener('load', () => {
    if (navigator.onLine) {
        syncTasksWithServer();
    }
});
