from django.db import models


class PossibleTask(models.Model):
    title = models.CharField(max_length=200, verbose_name='título')
    description = models.TextField(verbose_name='descrição')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Possível tarefa'
        verbose_name_plural = 'Possíveis tarefas'
        ordering = ['-created_at']

    def __str__(self):
        return self.title or self.description[:60]
