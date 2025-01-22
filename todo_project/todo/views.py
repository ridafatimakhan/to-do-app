from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session

from .models import Task

def welcome(request):
    return render(request, 'todo/welcome.html')

def todo_list_guest(request):
    # You can set up a temporary session for the guest user
    request.session['guest_user'] = 'guest_user'  # Assign a guest user key to the session
    return redirect('task_list')  # Redirect to the to-do list page

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
