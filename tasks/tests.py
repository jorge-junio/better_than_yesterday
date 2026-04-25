from datetime import date, datetime, timedelta, timezone as dt_timezone
from types import SimpleNamespace
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.test import RequestFactory, SimpleTestCase
from django.utils import timezone

from app.utils import htmx_redirect
from recurring_tasks.models import RecurringTask

from .models import Task
from .views import TaskCreateView, TaskTodayCompleteView
from .services import complete_task, ensure_tasks_for_date, get_today_mission_ordering, reopen_task, skip_task_for_today, start_task


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
        self.assertEqual(task.time_spent, timedelta(0))
        save_mock.assert_called_once()

    def test_task_completes_with_start_time_when_missing(self):
        task = Task(
            title='Estudar',
            scheduled_date=date(2026, 4, 22),
            task_type=Task.TaskType.TASK,
        )

        started_at = datetime(2026, 4, 22, 10, 0, tzinfo=dt_timezone.utc)
        finished_at = datetime(2026, 4, 22, 11, 30, 15, tzinfo=dt_timezone.utc)

        with patch('tasks.services.timezone.now', side_effect=[started_at, finished_at]), patch.object(Task, 'save') as save_mock:
            getattr(complete_task, '__wrapped__', complete_task)(task)

        self.assertTrue(task.is_completed)
        self.assertIsNotNone(task.started_in)
        self.assertIsNotNone(task.finished_in)
        self.assertEqual(task.time_spent, timedelta(hours=1, minutes=30, seconds=15))
        save_mock.assert_called_once()

    def test_task_completes_with_explicit_time_spent(self):
        task = Task(
            title='Estudar',
            scheduled_date=date(2026, 4, 22),
            task_type=Task.TaskType.TASK,
        )

        with patch('tasks.services.timezone.now', side_effect=[
            datetime(2026, 4, 22, 10, 0, tzinfo=dt_timezone.utc),
            datetime(2026, 4, 22, 10, 10, tzinfo=dt_timezone.utc),
        ]), patch.object(Task, 'save') as save_mock:
            getattr(complete_task, '__wrapped__', complete_task)(task, time_spent=timedelta(minutes=7, seconds=30))

        self.assertTrue(task.is_completed)
        self.assertEqual(task.time_spent, timedelta(minutes=7, seconds=30))
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

    def test_reopen_task_clears_completion_and_time_spent(self):
        task = Task(
            title='Treino',
            scheduled_date=date(2026, 4, 22),
            is_completed=True,
            completed_at=timezone.now(),
            finished_in=timezone.now(),
            time_spent=timedelta(minutes=42),
        )

        with patch.object(Task, 'save') as save_mock:
            getattr(reopen_task, '__wrapped__', reopen_task)(task)

        self.assertFalse(task.is_completed)
        self.assertIsNone(task.completed_at)
        self.assertIsNone(task.finished_in)
        self.assertIsNone(task.time_spent)
        save_mock.assert_called_once()

    def test_today_complete_requires_time_spent(self):
        request = RequestFactory().post('/tasks/today/1/complete/', data={}, HTTP_HX_REQUEST='true')
        request.user = SimpleNamespace(is_authenticated=True, has_perms=lambda perms: True)
        view = TaskTodayCompleteView.as_view()

        with patch('tasks.views.get_object_or_404') as get_object_mock, patch('tasks.views.services.get_today_mission_context') as context_mock:
            get_object_mock.return_value = Task(
                title='Treino',
                scheduled_date=date(2026, 4, 22),
            )
            context_mock.return_value = {'page_title': 'BTY - Missão do Dia'}

            response = view(request, pk=1)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Informe o tempo gasto para concluir a tarefa.', response.content.decode())
        get_object_mock.assert_called_once()
        context_mock.assert_called_once()

    def test_today_complete_allows_skip_time_with_flag(self):
        request = RequestFactory().post(
            '/tasks/today/1/complete/',
            data={'allow_without_time': '1'},
            HTTP_HX_REQUEST='true',
        )
        request.user = SimpleNamespace(is_authenticated=True, has_perms=lambda perms: True)
        view = TaskTodayCompleteView.as_view()

        task = Task(
            title='Treino',
            scheduled_date=date(2026, 4, 22),
        )

        with patch('tasks.views.get_object_or_404', return_value=task), patch('tasks.views.services.complete_task') as complete_mock, patch('tasks.views.services.get_today_mission_context') as context_mock:
            context_mock.return_value = {'page_title': 'BTY - Missão do Dia'}

            response = view(request, pk=1)

        self.assertEqual(response.status_code, 200)
        complete_mock.assert_called_once()
        kwargs = complete_mock.call_args.kwargs
        self.assertIsNone(kwargs['time_spent'])
        self.assertFalse(kwargs['record_time_spent'])


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


class HtmxRedirectTests(SimpleTestCase):
    def test_htmx_redirect_uses_success_status_and_header(self):
        response = htmx_redirect('/recurring-tasks/list/')

        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.headers['HX-Redirect'], '/recurring-tasks/list/')
