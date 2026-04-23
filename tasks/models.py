from django.core.exceptions import ValidationError
from django.db import models


class Task(models.Model):
    class SourceType(models.TextChoices):
        MANUAL = 'manual', 'Manual'
        RECURRENT = 'recurrent', 'Recorrente'

    title = models.CharField(max_length=500, verbose_name='título')
    description = models.TextField(null=True, blank=True, verbose_name='descrição')
    estimated_time = models.DurationField(null=True, blank=True, verbose_name='tempo estimado')
    scheduled_date = models.DateField(verbose_name='data')
    scheduled_time = models.TimeField(null=True, blank=True, verbose_name='horário')
    source_type = models.CharField(
        max_length=20,
        choices=SourceType.choices,
        default=SourceType.MANUAL,
        verbose_name='origem',
    )
    recurring_task = models.ForeignKey(
        'recurring_tasks.RecurringTask',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='generated_tasks',
        verbose_name='tarefa recorrente',
    )
    is_completed = models.BooleanField(default=False, verbose_name='concluída')
    started_in = models.DateTimeField(null=True, blank=True, editable=False, verbose_name='iniciada em')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='concluída em')
    finished_in = models.DateTimeField(null=True, blank=True, editable=False, verbose_name='finalizada em')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Tarefa'
        verbose_name_plural = 'Tarefas'
        ordering = ['scheduled_date', 'scheduled_time', 'title']
        constraints = [
            models.UniqueConstraint(
                fields=['scheduled_date', 'recurring_task'],
                name='task_recurring_date_uk',
            )
        ]

    def __str__(self):
        return f'{self.title} - {self.scheduled_date}'

    def clean(self):
        super().clean()

        if self.source_type == self.SourceType.RECURRENT and not self.recurring_task:
            raise ValidationError({'recurring_task': 'Tarefas recorrentes precisam de uma regra de origem.'})

        if self.recurring_task and self.source_type != self.SourceType.RECURRENT:
            self.source_type = self.SourceType.RECURRENT

    @property
    def is_pending(self):
        return not self.is_completed
