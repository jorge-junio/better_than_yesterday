from datetime import date, timedelta
from types import SimpleNamespace
from unittest import mock
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.test import RequestFactory, SimpleTestCase
from django.utils import timezone

from app.utils import htmx_redirect
from recurring_tasks.models import RecurringTask

from .models import Task
from .views import TaskCreateView, TaskListView, TaskTodayCompleteView
from .services import complete_task, ensure_tasks_for_date, get_today_mission_ordering, reopen_task, skip_task_for_today
from .templatetags.task_extras import duration_part


class TaskModelTests(SimpleTestCase):
    def test_manual_task_defaults_to_pending(self):
        task = Task(
            title='Comprar pão',
            scheduled_date=date(2026, 4, 22),
        )

        with patch('tasks.models.timezone.localdate', return_value=date(2026, 4, 22)):
            self.assertTrue(task.is_pending)
        self.assertEqual(task.priority, Task.Priority.LOW)

    def test_task_after_tomorrow_is_not_pending(self):
        task = Task(
            title='Comprar pão',
            scheduled_date=date(2026, 4, 24),
        )

        with patch('tasks.models.timezone.localdate', return_value=date(2026, 4, 22)):
            self.assertFalse(task.is_pending)

    def test_recurrent_task_requires_recurring_origin(self):
        task = Task(
            title='Academia',
            scheduled_date=date(2026, 4, 22),
            source_type=Task.SourceType.RECURRENT,
        )

        with self.assertRaises(ValidationError):
            task.clean()

    def test_complete_task_marks_completed(self):
        task = Task(
            title='Ler um capítulo',
            scheduled_date=date(2026, 4, 22),
        )

        with patch.object(Task, 'save') as save_mock, patch('tasks.services.timezone.now') as now_mock:
            now_mock.return_value = timezone.now()
            getattr(complete_task, '__wrapped__', complete_task)(task)

        self.assertTrue(task.is_completed)
        self.assertIsNotNone(task.completed_at)
        save_mock.assert_called_once()

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
        self.assertIsNotNone(task.completed_at)
        save_mock.assert_called_once()

    def test_reopen_task_clears_completion(self):
        task = Task(
            title='Treino',
            scheduled_date=date(2026, 4, 22),
            is_completed=True,
            completed_at=timezone.now(),
        )

        with patch.object(Task, 'save') as save_mock:
            getattr(reopen_task, '__wrapped__', reopen_task)(task)

        self.assertFalse(task.is_completed)
        self.assertIsNone(task.completed_at)
        save_mock.assert_called_once()

    def test_skipped_task_is_not_pending(self):
        task = Task(
            title='Reunião',
            scheduled_date=date(2026, 4, 22),
        )
        task.skipped_in = timezone.now()

        with patch('tasks.models.timezone.localdate', return_value=date(2026, 4, 22)):
            self.assertFalse(task.is_pending)
        self.assertTrue(task.is_skipped)

    def test_duration_part_splits_timedelta(self):
        value = timedelta(hours=2, minutes=5, seconds=9)

        self.assertEqual(duration_part(value, 'hours'), 2)
        self.assertEqual(duration_part(value, 'minutes'), 5)
        self.assertEqual(duration_part(value, 'seconds'), 9)
        self.assertEqual(duration_part(None, 'hours'), 0)

    def test_today_complete_calls_complete_task_without_time_input(self):
        request = RequestFactory().post(
            '/tasks/today/1/complete/?scheduled_date=2026-04-21',
            HTTP_HX_REQUEST='true',
        )
        request.user = SimpleNamespace(is_authenticated=True, has_perms=lambda perms: True)
        view = TaskTodayCompleteView.as_view()

        task = Task(
            title='Treino',
            scheduled_date=date(2026, 4, 22),
        )

        with patch('tasks.views.get_object_or_404', return_value=task) as get_object_mock, patch('tasks.views.services.complete_task') as complete_mock, patch('tasks.views.services.get_today_mission_context') as context_mock, patch('tasks.views.render') as render_mock:
            context_mock.return_value = {'page_title': 'BTY - Missão do Dia'}
            render_mock.return_value = HttpResponse('ok')

            response = view(request, pk=1)

        self.assertEqual(response.status_code, 200)
        get_object_mock.assert_called_once_with(Task, pk=1, scheduled_date=date(2026, 4, 21))
        context_mock.assert_called_once()
        complete_mock.assert_called_once()
        self.assertFalse(complete_mock.call_args.kwargs)
        render_mock.assert_called_once()
        self.assertEqual(render_mock.call_args.args[2]['selected_date'], date(2026, 4, 21))


class RecurrenceGenerationTests(SimpleTestCase):
    def test_generation_service_signature_exists(self):
        recurring_task = RecurringTask(
            name='Academia',
            recurrence_type=RecurringTask.RecurrenceType.WEEKDAYS,
            weekdays=['wed'],
        )

        self.assertTrue(hasattr(recurring_task, 'occurs_on'))
        self.assertTrue(callable(ensure_tasks_for_date))

    def test_today_mission_orders_by_priority_title(self):
        ordering = get_today_mission_ordering()

        self.assertEqual(len(ordering), 2)
        self.assertEqual(str(ordering[0]), 'OrderBy(F(priority), descending=True)')
        self.assertEqual(ordering[1], 'title')


class TaskCreateViewTests(SimpleTestCase):
    def test_prefills_description_from_querystring(self):
        request = RequestFactory().get('/tasks/create/?description=Comprar+leite')
        view = TaskCreateView()
        view.request = request

        self.assertEqual(view.get_initial()['description'], 'Comprar leite')

    def test_prefills_possible_task_data(self):
        request = RequestFactory().get('/tasks/create/?possible_task=7')
        view = TaskCreateView()
        view.request = request

        possible_task = SimpleNamespace(
            title='Comprar pão',
            description='Ir à padaria',
            priority=Task.Priority.HIGH,
        )

        with patch('tasks.views.possible_task_services.get_possible_task', return_value=possible_task):
            initial = view.get_initial()

        self.assertEqual(initial['title'], 'Comprar pão')
        self.assertEqual(initial['description'], 'Ir à padaria')
        self.assertEqual(initial['priority'], Task.Priority.HIGH)


class TaskListViewTests(SimpleTestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

    def test_filters_by_title_and_description(self):
        request = self.request_factory.get(
            '/tasks/list/',
            {'title': 'reunião', 'description': 'status'},
        )
        request.user = SimpleNamespace(is_authenticated=True, has_perms=lambda perms: True)
        view = TaskListView()
        view.request = request

        base_queryset = mock.Mock()
        date_queryset = mock.Mock()
        title_queryset = mock.Mock()
        description_queryset = mock.Mock()
        final_queryset = mock.Mock()
        base_queryset.filter.return_value = date_queryset
        date_queryset.filter.return_value = title_queryset
        title_queryset.filter.return_value = description_queryset
        description_queryset.select_related.return_value = final_queryset

        with patch('tasks.views.services.ensure_tasks_for_date') as ensure_mock, patch.object(Task._default_manager, 'all', return_value=base_queryset):
            queryset = view.get_queryset()

        ensure_mock.assert_called_once()
        date_queryset.filter.assert_called_once_with(title__icontains='reunião')
        title_queryset.filter.assert_called_once_with(description__icontains='status')
        description_queryset.select_related.assert_called_once_with('recurring_task', 'category')
        self.assertIs(queryset, final_queryset)


class HtmxRedirectTests(SimpleTestCase):
    def test_htmx_redirect_uses_success_status_and_header(self):
        response = htmx_redirect('/recurring-tasks/list/')

        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.headers['HX-Redirect'], '/recurring-tasks/list/')
