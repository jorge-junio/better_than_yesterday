from datetime import date
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from django.core.exceptions import ValidationError
from django.test import RequestFactory, SimpleTestCase

from .models import RecurringTask
from .forms import RecurringTaskForm
from .views import RecurringTaskCreateView, RecurringTaskUpdateView
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


class RecurringTaskFormTests(SimpleTestCase):
    def test_specific_dates_initial_is_rendered_as_multiline_text(self):
        recurring_task = RecurringTask(
            name='Revisão',
            recurrence_type=RecurringTask.RecurrenceType.SPECIFIC_DATES,
            specific_dates=['2027-01-01', '2027-01-02'],
        )
        recurring_task.pk = 1

        form = RecurringTaskForm(instance=recurring_task)

        self.assertEqual(form.initial['specific_dates'], '2027-01-01\n2027-01-02')


class RecurringTaskUpdateViewTests(SimpleTestCase):
    def test_form_valid_returns_htmx_redirect_for_htmx_requests(self):
        request = RequestFactory().post('/recurring-tasks/1/update/', HTTP_HX_REQUEST='true')
        view = RecurringTaskUpdateView()
        view.request = request

        form = MagicMock()
        saved_object = SimpleNamespace(pk=1)
        form.save.return_value = saved_object

        with patch('recurring_tasks.views.htmx_redirect') as redirect_mock:
            redirect_response = MagicMock()
            redirect_mock.return_value = redirect_response

            response = view.form_valid(form)

        self.assertIs(response, redirect_response)
        form.save.assert_called_once()
        redirect_mock.assert_called_once_with(view.get_success_url())


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

    def test_sync_generated_tasks_raises_validation_error_when_update_fails(self):
        recurring_task = SimpleNamespace(
            pk=1,
            name='Academia',
            description='Treino na academia',
            estimated_time=None,
            task_type=RecurringTask.TaskType.TASK,
            priority=RecurringTask.Priority.HIGH,
            generated_tasks=MagicMock(),
        )

        recurring_task.generated_tasks.update.side_effect = RuntimeError('boom')

        with self.assertRaises(ValidationError):
            getattr(
                sync_generated_tasks_from_recurring_task,
                '__wrapped__',
                sync_generated_tasks_from_recurring_task,
            )(recurring_task)
