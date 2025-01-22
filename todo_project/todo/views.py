from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Task

def welcome(request):
    return render(request, 'todo/welcome.html')

@login_required
def task_list(request):
    tasks = request.user.task_set.all()  # Filter tasks by logged-in user
    return render(request, 'todo/task_list.html', {'tasks': tasks})

@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST['title']
        request.user.task_set.create(title=title)
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
