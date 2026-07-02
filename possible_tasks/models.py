from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class PossibleTask(models.Model):
    class Priority(models.IntegerChoices):
        LOW = 1, 'Baixa'
        MEDIUM = 2, 'Média'
        HIGH = 3, 'Alta'

    title = models.CharField(max_length=200, verbose_name='título')
    description = models.TextField(verbose_name='descrição')
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='possible_tasks',
        verbose_name='projeto',
    )
    priority = models.PositiveSmallIntegerField(
        choices=Priority.choices,
        default=Priority.LOW,
        verbose_name='prioridade',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Possível tarefa'
        verbose_name_plural = 'Possíveis tarefas'
        ordering = ['-priority', 'title']

    def __str__(self):
        return self.title or self.description[:60]

    @property
    def generated_object(self):
        for attr in ('generated_task', 'generated_recurring_task', 'generated_project_task'):
            try:
                generated = getattr(self, attr)
            except ObjectDoesNotExist:
                continue
            if generated is not None:
                return generated
        return None

    @property
    def generated_type_label(self):
        generated = self.generated_object
        if generated is None:
            return ''
        if generated.__class__.__name__ == 'Task':
            return 'Tarefa'
        if generated.__class__.__name__ == 'RecurringTask':
            return 'Tarefa recorrente'
        if generated.__class__.__name__ == 'ProjectTask':
            return 'Tarefa de projeto'
        return 'Gerado'
