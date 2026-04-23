from django.db import transaction
from django.utils import timezone


@transaction.atomic
def complete_project_task(project_task):
    project_task.status = project_task.Status.COMPLETED
    project_task.completion_percentage = 100
    project_task.completed_at = project_task.completed_at or timezone.now()
    project_task.save(update_fields=['status', 'completion_percentage', 'completed_at', 'updated_at'])
    return project_task


@transaction.atomic
def reopen_project_task(project_task):
    project_task.status = project_task.Status.PENDING
    project_task.completion_percentage = 0
    project_task.completed_at = None
    project_task.save(update_fields=['status', 'completion_percentage', 'completed_at', 'updated_at'])
    return project_task
