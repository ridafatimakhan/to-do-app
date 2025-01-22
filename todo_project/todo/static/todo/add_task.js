document.getElementById('taskForm').addEventListener('submit', function (event) {
    event.preventDefault();

    const title = document.getElementById('taskTitle').value;
    const category = document.getElementById('category').value;
    const priority = document.getElementById('priority').value;

    const task = {
        title: title,
        category: category,
        priority: priority,
        completed: false,
    };

    // Save task to localStorage for offline functionality
    let tasks = JSON.parse(localStorage.getItem('tasks')) || [];
    tasks.push(task);
    localStorage.setItem('tasks', JSON.stringify(tasks));

    // You can also show the task locally to the user
    displayTask(task);

    // Sync tasks with server when online
    if (navigator.onLine) {
        syncTasksWithServer();
    }
});

// Sync tasks with the server when the user is online
function syncTasksWithServer() {
    const tasks = JSON.parse(localStorage.getItem('tasks')) || [];
    fetch('/api/tasks/', {
        method: 'POST',
        body: JSON.stringify(tasks),
        headers: {
            'Content-Type': 'application/json',
        },
    }).then(response => response.json())
        .then(data => {
            console.log('Tasks synced with server:', data);
            localStorage.removeItem('tasks'); // Clear localStorage after sync
        })
        .catch(error => {
            console.log('Syncing failed, try again later:', error);
        });
}

// Listen for online events to trigger syncing
window.addEventListener('online', () => {
    console.log('You are online');
    syncTasksWithServer();
});
