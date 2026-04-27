# Generated manually to remove the task type field now that all tasks are treated as objectives.

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0008_task_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='task_type',
        ),
    ]

