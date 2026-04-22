from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from recurring_tasks.models import RecurringTask

from .models import Task


def ensure_tasks_for_date(target_date):
    recurring_tasks = RecurringTask.objects.filter(is_active=True)
    created = 0

    for recurring_task in recurring_tasks:
        if not recurring_task.occurs_on(target_date):
            continue

        _, was_created = Task.objects.get_or_create(
            scheduled_date=target_date,
            recurring_task=recurring_task,
            defaults={
                'title': recurring_task.name,
                'description': recurring_task.description,
                'source_type': Task.SourceType.RECURRENT,
            },
        )
        if was_created:
            created += 1

    return created


@transaction.atomic
def complete_task(task):
    if not task.is_completed:
        task.is_completed = True
        task.completed_at = timezone.now()
        task.save(update_fields=['is_completed', 'completed_at', 'updated_at'])
    return task


@transaction.atomic
def reopen_task(task):
    if task.is_completed:
        task.is_completed = False
        task.completed_at = None
        task.save(update_fields=['is_completed', 'completed_at', 'updated_at'])
    return task


@transaction.atomic
def postpone_task(task, days=1):
    task.scheduled_date = task.scheduled_date + timedelta(days=days)
    task.save(update_fields=['scheduled_date', 'updated_at'])
    return task
