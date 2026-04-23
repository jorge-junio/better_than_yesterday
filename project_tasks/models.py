from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class ProjectTask(models.Model):
    class Priority(models.IntegerChoices):
        LOW = 1, 'Baixa'
        MEDIUM = 2, 'Média'
        HIGH = 3, 'Alta'

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pendente'
        COMPLETED = 'completed', 'Concluída'

    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='project_tasks',
        verbose_name='projeto',
    )
    title = models.CharField(max_length=200, verbose_name='título')
    description = models.TextField(verbose_name='descrição')
    priority = models.PositiveSmallIntegerField(
        choices=Priority.choices,
        default=Priority.LOW,
        verbose_name='prioridade',
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name='status',
    )
    completion_percentage = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='porcentagem de conclusão',
    )
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='concluída em')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Tarefa de projeto'
        verbose_name_plural = 'Tarefas de projeto'
        ordering = ['-priority', 'title']

    def __str__(self):
        return f'{self.title} - {self.project.title}'

    @property
    def is_completed(self):
        return self.status == self.Status.COMPLETED

    def clean(self):
        super().clean()

        if self.completion_percentage >= 100:
            self.completion_percentage = 100
            self.status = self.Status.COMPLETED
        elif self.status == self.Status.COMPLETED:
            self.completion_percentage = 100

    def save(self, *args, **kwargs):
        if self.status == self.Status.COMPLETED or self.completion_percentage >= 100:
            self.status = self.Status.COMPLETED
            self.completion_percentage = 100
            if self.completed_at is None:
                self.completed_at = timezone.now()
        else:
            self.completed_at = None

        super().save(*args, **kwargs)
