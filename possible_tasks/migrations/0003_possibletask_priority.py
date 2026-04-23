from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('possible_tasks', '0002_possibletask_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='possibletask',
            name='priority',
            field=models.PositiveSmallIntegerField(
                choices=[(1, 'Baixa'), (2, 'Média'), (3, 'Alta')],
                default=1,
                verbose_name='prioridade',
            ),
        ),
        migrations.AlterModelOptions(
            name='possibletask',
            options={'ordering': ['-priority', 'title'], 'verbose_name': 'Possível tarefa', 'verbose_name_plural': 'Possíveis tarefas'},
        ),
    ]
