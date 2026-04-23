from django.db import migrations, models


def populate_titles(apps, schema_editor):
    PossibleTask = apps.get_model('possible_tasks', 'PossibleTask')

    for possible_task in PossibleTask.objects.all():
        if possible_task.title:
            continue

        description = (possible_task.description or '').strip()
        first_line = description.splitlines()[0].strip() if description else ''
        possible_task.title = first_line[:200] or 'Sem título'
        possible_task.save(update_fields=['title'])


class Migration(migrations.Migration):

    dependencies = [
        ('possible_tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='possibletask',
            name='title',
            field=models.CharField(default='', max_length=200, verbose_name='título'),
            preserve_default=False,
        ),
        migrations.RunPython(populate_titles, migrations.RunPython.noop),
    ]
