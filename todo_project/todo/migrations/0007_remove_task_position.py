# Generated by Django 5.0.7 on 2025-01-22 22:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0006_task_position'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='position',
        ),
    ]
