from datetime import date
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import RequestFactory, SimpleTestCase
from django.utils import timezone

from recurring_tasks.models import RecurringTask

from .models import Task
from .views import TaskCreateView
from .services import complete_task, ensure_tasks_for_date, get_today_mission_ordering, skip_task_for_today, start_task


class TaskModelTests(SimpleTestCase):
    def test_manual_task_defaults_to_pending(self):
        task = Task(
            title='Comprar pão',
            scheduled_date=date(2026, 4, 22),
        )

        self.assertTrue(task.is_pending)
        self.assertEqual(task.task_type, Task.TaskType.TASK)
        self.assertEqual(task.priority, Task.Priority.LOW)

    def test_recurrent_task_requires_recurring_origin(self):
        task = Task(
            title='Academia',
            scheduled_date=date(2026, 4, 22),
            source_type=Task.SourceType.RECURRENT,
        )

        with self.assertRaises(ValidationError):
            task.clean()

    def test_objective_completes_without_starting(self):
        task = Task(
            title='Ler um capítulo',
            scheduled_date=date(2026, 4, 22),
            task_type=Task.TaskType.OBJECTIVE,
        )

        with patch.object(Task, 'save') as save_mock:
            getattr(complete_task, '__wrapped__', complete_task)(task)

        self.assertTrue(task.is_completed)
        self.assertIsNone(task.started_in)
        self.assertIsNotNone(task.finished_in)
        save_mock.assert_called_once()

    def test_task_completes_with_start_time_when_missing(self):
        task = Task(
            title='Estudar',
            scheduled_date=date(2026, 4, 22),
            task_type=Task.TaskType.TASK,
        )

        with patch.object(Task, 'save') as save_mock:
            getattr(complete_task, '__wrapped__', complete_task)(task)

        self.assertTrue(task.is_completed)
        self.assertIsNotNone(task.started_in)
        self.assertIsNotNone(task.finished_in)
        save_mock.assert_called_once()

    def test_start_task_is_ignored_for_objective(self):
        task = Task(
            title='Escrever meta',
            scheduled_date=date(2026, 4, 22),
            task_type=Task.TaskType.OBJECTIVE,
        )

        with patch.object(Task, 'save') as save_mock:
            getattr(start_task, '__wrapped__', start_task)(task)

        self.assertIsNone(task.started_in)
        save_mock.assert_not_called()

    def test_skipped_task_is_not_pending(self):
        task = Task(
            title='Reunião',
            scheduled_date=date(2026, 4, 22),
        )
        task.skipped_in = timezone.now()

        self.assertFalse(task.is_pending)
        self.assertTrue(task.is_skipped)

    def test_skip_task_for_today_marks_skip_flag(self):
        task = Task(
            title='Treino',
            scheduled_date=date(2026, 4, 22),
        )

        with patch.object(Task, 'save') as save_mock:
            getattr(skip_task_for_today, '__wrapped__', skip_task_for_today)(task)

        self.assertIsNotNone(task.skipped_in)
        save_mock.assert_called_once()

    def test_complete_task_clears_skip_flag(self):
        task = Task(
            title='Treino',
            scheduled_date=date(2026, 4, 22),
            skipped_in=timezone.now(),
        )

        with patch.object(Task, 'save') as save_mock:
            getattr(complete_task, '__wrapped__', complete_task)(task)

        self.assertIsNone(task.skipped_in)
        self.assertTrue(task.is_completed)
        save_mock.assert_called_once()


class RecurrenceGenerationTests(SimpleTestCase):
    def test_generation_service_signature_exists(self):
        recurring_task = RecurringTask(
            name='Academia',
            recurrence_type=RecurringTask.RecurrenceType.WEEKDAYS,
            weekdays=['wed'],
        )

        self.assertTrue(hasattr(recurring_task, 'occurs_on'))
        self.assertTrue(callable(ensure_tasks_for_date))
        self.assertEqual(recurring_task.task_type, RecurringTask.TaskType.TASK)

    def test_today_mission_orders_by_started_priority_title(self):
        ordering = get_today_mission_ordering()

        self.assertEqual(len(ordering), 3)
        self.assertEqual(str(ordering[0]), 'OrderBy(F(started_in), descending=True)')
        self.assertEqual(str(ordering[1]), 'OrderBy(F(priority), descending=True)')
        self.assertEqual(ordering[2], 'title')


class TaskCreateViewTests(SimpleTestCase):
    def test_prefills_description_from_querystring(self):
        request = RequestFactory().get('/tasks/create/?description=Comprar+leite')
        view = TaskCreateView()
        view.request = request

        self.assertEqual(view.get_initial()['description'], 'Comprar leite')
