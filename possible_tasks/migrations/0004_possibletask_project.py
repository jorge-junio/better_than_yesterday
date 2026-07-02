import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
        ('possible_tasks', '0003_possibletask_priority'),
    ]

    operations = [
        migrations.AddField(
            model_name='possibletask',
            name='project',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='possible_tasks',
                to='projects.project',
                verbose_name='projeto',
            ),
        ),
    ]
