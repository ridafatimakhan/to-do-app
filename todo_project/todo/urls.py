from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('tasks/', views.task_list, name='task_list'),
    path('add/', views.add_task, name='add_task'),
    path('complete/<int:task_id>/', views.complete_task, name='complete_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    # User Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='todo/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('task-list-guest/', views.task_list_guest, name='task_list_guest'),  # Guest task list
    path('todo-list-guest/', views.todo_list_guest, name='todo_list_guest'),  # For guest users to access the list
    path('add-task-guest/', views.add_task_guest, name='add_task_guest'),
    path('delete-task-guest/<int:task_index>/', views.delete_task_guest, name='delete_task_guest'),
    path('complete-task-guest/<int:task_index>/', views.complete_task_guest, name='complete_task_guest'),
    path('api/tasks/', views.sync_tasks, name='sync_tasks'),


]
