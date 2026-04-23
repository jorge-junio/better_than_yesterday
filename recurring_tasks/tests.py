from datetime import date
from types import SimpleNamespace
from unittest.mock import MagicMock

from django.core.exceptions import ValidationError
from django.test import RequestFactory, SimpleTestCase

from .models import RecurringTask
from .views import RecurringTaskCreateView
from .services import sync_generated_tasks_from_recurring_task


class RecurringTaskModelTests(SimpleTestCase):
    def test_weekday_recurrence_matches_selected_day(self):
        task = RecurringTask(
            name='Academia',
            recurrence_type=RecurringTask.RecurrenceType.WEEKDAYS,
            weekdays=['mon', 'wed'],
        )

        task.clean()

        self.assertTrue(task.occurs_on(date(2026, 4, 22)))
        self.assertFalse(task.occurs_on(date(2026, 4, 23)))

    def test_date_range_requires_boundaries(self):
        task = RecurringTask(
            name='Projeto',
            recurrence_type=RecurringTask.RecurrenceType.DATE_RANGE,
        )

        with self.assertRaises(ValidationError):
            task.clean()

    def test_specific_dates_are_normalized_and_checked(self):
        task = RecurringTask(
            name='Revisão',
            recurrence_type=RecurringTask.RecurrenceType.SPECIFIC_DATES,
            specific_dates=['2026-04-22', '2026-04-24'],
        )

        task.clean()

        self.assertEqual(task.specific_dates, ['2026-04-22', '2026-04-24'])
        self.assertTrue(task.occurs_on(date(2026, 4, 24)))
        self.assertFalse(task.occurs_on(date(2026, 4, 23)))

    def test_defaults_to_task_type(self):
        task = RecurringTask(
            name='Academia',
            recurrence_type=RecurringTask.RecurrenceType.WEEKDAYS,
            weekdays=['mon'],
        )

        self.assertEqual(task.task_type, RecurringTask.TaskType.TASK)
        self.assertEqual(task.priority, RecurringTask.Priority.LOW)


class RecurringTaskCreateViewTests(SimpleTestCase):
    def test_prefills_description_from_querystring(self):
        request = RequestFactory().get('/recurring-tasks/create/?description=Fazer+alongamento')
        view = RecurringTaskCreateView()
        view.request = request

        self.assertEqual(view.get_initial()['description'], 'Fazer alongamento')


class RecurringTaskSyncTests(SimpleTestCase):
    def test_sync_generated_tasks_updates_priority_and_related_fields(self):
        recurring_task = SimpleNamespace(
            pk=1,
            name='Academia',
            description='Treino na academia',
            estimated_time=None,
            task_type=RecurringTask.TaskType.TASK,
            priority=RecurringTask.Priority.HIGH,
            generated_tasks=MagicMock(),
        )

        update_mock = MagicMock(return_value=2)
        recurring_task.generated_tasks.update = update_mock

        updated = getattr(
            sync_generated_tasks_from_recurring_task,
            '__wrapped__',
            sync_generated_tasks_from_recurring_task,
        )(recurring_task)

        self.assertEqual(updated, 2)
        update_mock.assert_called_once()
        kwargs = update_mock.call_args.kwargs
        self.assertEqual(kwargs['priority'], RecurringTask.Priority.HIGH)
        self.assertEqual(kwargs['task_type'], RecurringTask.TaskType.TASK)
