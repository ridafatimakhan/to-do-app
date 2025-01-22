from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.http import HttpResponse
from .models import Task

def welcome(request):
    return render(request, 'todo/welcome.html')


def todo_list_guest(request):
    # Create a temporary session for the guest user (no need for authentication)
    request.session['guest_user'] = 'guest_user'  # Set a flag indicating a guest user
    
    # Initialize a temporary task list for the guest user
    if 'guest_tasks' not in request.session:
        request.session['guest_tasks'] = []  # Initialize an empty list for guest tasks
    
    # Redirect the guest user to the to-do list page
    return redirect('task_list_guest')  # Redirect to the task list page for guests

def task_list_guest(request):
    # Get the guest user tasks from the session
    guest_tasks = request.session.get('guest_tasks', [])
    
    # Optionally, you can also handle filtering logic similar to the authenticated user
    
    return render(request, 'todo/task_list_guest.html', {'tasks': guest_tasks})

@login_required
def task_list(request):
    tasks = request.user.task_set.all()  # Get all tasks for the user

    # Filter tasks by category if provided in the request
    category_filter = request.GET.get('category')
    if category_filter:
        tasks = tasks.filter(category=category_filter)

    # Filter tasks by priority if provided in the request
    priority_filter = request.GET.get('priority')
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)

    return render(request, 'todo/task_list.html', {'tasks': tasks})




def add_task_guest(request):
    if request.method == 'POST':
        task_name = request.POST['task_name']
        category = request.POST['category']
        priority = request.POST['priority']
        
        task = {'name': task_name, 'category': category, 'priority': priority}
        
        guest_tasks = request.session.get('guest_tasks', [])
        guest_tasks.append(task)
        
        request.session['guest_tasks'] = guest_tasks
        
        return redirect('task_list_guest')
    else:
        return render(request, 'todo/add_task_guest.html')


def delete_task_guest(request, task_index):
    # Fetch tasks from the session
    guest_tasks = request.session.get('guest_tasks', [])

    # Check if the task_index is valid
    if 0 <= task_index < len(guest_tasks):
        del guest_tasks[task_index]  # Delete the task at the provided index
    
    # Save the updated tasks back to the session
    request.session['guest_tasks'] = guest_tasks
    
    # Redirect to the task list page
    return redirect('task_list_guest')

def complete_task_guest(request, task_index):
    # You can find the task based on the index (or use another identifier if needed)
    tasks = request.session.get('guest_tasks', [])
    if tasks:
        task = tasks[task_index]
        task['completed'] = True  # Set the task as completed
        # Save the updated list of tasks back to the session
        request.session['guest_tasks'] = tasks
    return redirect('task_list_guest')
    
@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST['title']
        category = request.POST['category']
        priority = request.POST['priority']
        request.user.task_set.create(title=title, category=category, priority=priority)
        return redirect('task_list')
    return render(request, 'todo/add_task.html')


@login_required
def complete_task(request, task_id):
    task = request.user.task_set.get(id=task_id)
    task.completed = True
    task.save()
    return redirect('task_list')

@login_required
def delete_task(request, task_id):
    task = request.user.task_set.get(id=task_id)
    task.delete()
    return redirect('task_list')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in after signup
            return redirect('task_list')
    else:
        form = UserCreationForm()
    return render(request, 'todo/signup.html', {'form': form})

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def sync_tasks(request):
    if request.method == 'POST':
        tasks_data = json.loads(request.body)
        # Logic to save tasks to the database
        for task in tasks_data:
            # You can process the tasks here
            pass
        return JsonResponse({"status": "success", "message": "Tasks synced!"})

