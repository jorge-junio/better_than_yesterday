# Generated manually to remove the task type field now that all recurring tasks are treated as objectives.

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recurring_tasks', '0005_recurringtask_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recurringtask',
            name='task_type',
        ),
    ]

