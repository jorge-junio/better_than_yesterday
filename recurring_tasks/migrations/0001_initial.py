from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='RecurringTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='nome')),
                ('description', models.TextField(blank=True, null=True, verbose_name='descrição')),
                (
                    'recurrence_type',
                    models.CharField(
                        choices=[
                            ('weekdays', 'Dias da semana'),
                            ('date_range', 'Intervalo de datas'),
                            ('specific_dates', 'Datas específicas'),
                        ],
                        max_length=20,
                        verbose_name='tipo de recorrência',
                    ),
                ),
                ('weekdays', models.JSONField(blank=True, default=list, verbose_name='dias da semana')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='data inicial')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='data final')),
                ('specific_dates', models.JSONField(blank=True, default=list, verbose_name='datas específicas')),
                ('is_active', models.BooleanField(default=True, verbose_name='ativo')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Tarefa recorrente',
                'verbose_name_plural': 'Tarefas recorrentes',
                'ordering': ['name'],
            },
        ),
        migrations.AddConstraint(
            model_name='recurringtask',
            constraint=models.UniqueConstraint(fields=('name',), name='recurring_task_name_uk'),
        ),
    ]
