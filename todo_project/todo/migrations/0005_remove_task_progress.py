# Generated by Django 5.0.7 on 2025-01-22 19:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0004_task_progress'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='progress',
        ),
    ]
