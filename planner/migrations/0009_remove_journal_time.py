# Generated by Django 4.1 on 2022-08-19 14:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0008_alter_event_updated_at_alter_task_updated_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='journal',
            name='time',
        ),
    ]
