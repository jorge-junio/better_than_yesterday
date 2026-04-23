from django.db import transaction
from django.utils import timezone


@transaction.atomic
def sync_generated_tasks_from_recurring_task(recurring_task):
    if not recurring_task.pk:
        return 0

    return recurring_task.generated_tasks.update(
        title=recurring_task.name,
        description=recurring_task.description,
        estimated_time=recurring_task.estimated_time,
        task_type=recurring_task.task_type,
        priority=recurring_task.priority,
        updated_at=timezone.now(),
    )
