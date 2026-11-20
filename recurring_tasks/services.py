import logging

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

logger = logging.getLogger(__name__)


@transaction.atomic
def sync_generated_tasks_from_recurring_task(recurring_task):
    try:
        if not recurring_task.pk:
            return 0

        updated = recurring_task.generated_tasks.update(
            title=recurring_task.name,
            description=recurring_task.description,
            estimated_time=recurring_task.estimated_time,
            priority=recurring_task.priority,
            category=recurring_task.category,
            updated_at=timezone.now(),
        )
        recurring_task.generated_tasks.filter(completed_at__isnull=True).update(
            skill=recurring_task.skill,
            scheduled_time=recurring_task.scheduled_time,
        )
        return updated
    except Exception as exc:
        logger.exception(
            'Erro ao sincronizar tasks geradas da recurring task %s',
            getattr(recurring_task, 'pk', None),
        )
        raise ValidationError('Erro ao sincronizar tasks geradas.') from exc
