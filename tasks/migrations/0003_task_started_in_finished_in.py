from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_tempo_estimado'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='started_in',
            field=models.DateTimeField(blank=True, editable=False, null=True, verbose_name='iniciada em'),
        ),
        migrations.AddField(
            model_name='task',
            name='finished_in',
            field=models.DateTimeField(blank=True, editable=False, null=True, verbose_name='finalizada em'),
        ),
    ]
