from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recurring_tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recurringtask',
            name='estimated_time',
            field=models.DurationField(blank=True, null=True, verbose_name='estimated time'),
        ),
    ]
