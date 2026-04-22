from datetime import date

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from recurring_tasks.models import RecurringTask

from .models import Task
from .services import ensure_tasks_for_date


class TaskModelTests(SimpleTestCase):
    def test_manual_task_defaults_to_pending(self):
        task = Task(
            title='Comprar pão',
            scheduled_date=date(2026, 4, 22),
        )

        self.assertTrue(task.is_pending)

    def test_recurrent_task_requires_recurring_origin(self):
        task = Task(
            title='Academia',
            scheduled_date=date(2026, 4, 22),
            source_type=Task.SourceType.RECURRENT,
        )

        with self.assertRaises(ValidationError):
            task.clean()


class RecurrenceGenerationTests(SimpleTestCase):
    def test_generation_service_signature_exists(self):
        recurring_task = RecurringTask(
            name='Academia',
            recurrence_type=RecurringTask.RecurrenceType.WEEKDAYS,
            weekdays=['wed'],
        )

        self.assertTrue(hasattr(recurring_task, 'occurs_on'))
        self.assertTrue(callable(ensure_tasks_for_date))
