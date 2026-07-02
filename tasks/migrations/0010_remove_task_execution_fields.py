from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0009_remove_task_task_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='started_in',
        ),
        migrations.RemoveField(
            model_name='task',
            name='finished_in',
        ),
        migrations.RemoveField(
            model_name='task',
            name='time_spent',
        ),
    ]
