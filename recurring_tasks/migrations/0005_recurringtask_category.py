# Generated manually to add category support to recurring tasks.

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
        ('recurring_tasks', '0004_recurringtask_priority'),
    ]

    operations = [
        migrations.AddField(
            model_name='recurringtask',
            name='category',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='recurring_tasks',
                to='categories.category',
                verbose_name='categoria',
            ),
        ),
    ]

