from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recurring_tasks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, verbose_name='título')),
                ('description', models.TextField(blank=True, null=True, verbose_name='descrição')),
                ('scheduled_date', models.DateField(verbose_name='data')),
                ('scheduled_time', models.TimeField(blank=True, null=True, verbose_name='horário')),
                (
                    'source_type',
                    models.CharField(
                        choices=[('manual', 'Manual'), ('recurrent', 'Recorrente')],
                        default='manual',
                        max_length=20,
                        verbose_name='origem',
                    ),
                ),
                ('is_completed', models.BooleanField(default=False, verbose_name='concluída')),
                ('completed_at', models.DateTimeField(blank=True, null=True, verbose_name='concluída em')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                (
                    'recurring_task',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='generated_tasks',
                        to='recurring_tasks.recurringtask',
                        verbose_name='tarefa recorrente',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Tarefa',
                'verbose_name_plural': 'Tarefas',
                'ordering': ['scheduled_date', 'scheduled_time', 'title'],
            },
        ),
        migrations.AddConstraint(
            model_name='task',
            constraint=models.UniqueConstraint(fields=('scheduled_date', 'recurring_task'), name='task_recurring_date_uk'),
        ),
    ]
