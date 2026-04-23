from django.db import models


class PossibleTask(models.Model):
    class Priority(models.IntegerChoices):
        LOW = 1, 'Baixa'
        MEDIUM = 2, 'Média'
        HIGH = 3, 'Alta'

    title = models.CharField(max_length=200, verbose_name='título')
    description = models.TextField(verbose_name='descrição')
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
