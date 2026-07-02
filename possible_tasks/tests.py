from datetime import date
from unittest import mock
from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase
from django.urls import reverse

from .models import PossibleTask
from .services import link_possible_task_to_generated_object
from .views import PossibleTaskCreateView, PossibleTaskDetailView, PossibleTaskListView
from project_tasks.models import ProjectTask
from recurring_tasks.models import RecurringTask
from tasks.models import Task


class PossibleTaskModelTests(SimpleTestCase):
    def test_str_returns_title(self):
        task = PossibleTask(title='Organizar estação', description='Organizar mesa de trabalho')

        self.assertEqual(str(task), 'Organizar estação')

    def test_defaults_to_low_priority(self):
        task = PossibleTask(title='Organizar estação', description='Organizar mesa de trabalho')

        self.assertEqual(task.priority, PossibleTask.Priority.LOW)

    def test_project_is_optional(self):
        field = PossibleTask._meta.get_field('project')

        self.assertTrue(field.null)
        self.assertTrue(field.blank)

    def test_generated_origin_fields_exist(self):
        self.assertTrue(Task._meta.get_field('origin_possible_task').null)
        self.assertTrue(RecurringTask._meta.get_field('origin_possible_task').null)
        self.assertTrue(ProjectTask._meta.get_field('origin_possible_task').null)

    def test_link_possible_task_to_generated_object_sets_origin(self):
        possible_task = PossibleTask(title='Organizar estação', description='Organizar mesa de trabalho')
        task = Task(title='Organizar estação', scheduled_date=date(2026, 4, 22))

        with patch.object(Task, 'save') as save_mock:
            link_possible_task_to_generated_object(possible_task, task)

        self.assertIs(task.origin_possible_task, possible_task)
        save_mock.assert_called_once()


class PossibleTaskUrlTests(SimpleTestCase):
    def test_list_urls_exist(self):
        self.assertEqual(reverse('possible_task_list'), '/possible-tasks/list/')
        self.assertEqual(reverse('possible_task_create'), '/possible-tasks/create/')
        self.assertEqual(reverse('possible_task_detail', args=[1]), '/possible-tasks/1/detail/')
        self.assertEqual(reverse('possible_task_update', args=[1]), '/possible-tasks/1/update/')
        self.assertEqual(reverse('possible_task_delete', args=[1]), '/possible-tasks/1/delete/')


class PossibleTaskDetailViewTests(SimpleTestCase):
    def test_view_uses_detail_template(self):
        self.assertEqual(PossibleTaskDetailView.template_name, 'possible_task_detail.html')


class PossibleTaskListViewTests(SimpleTestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

    def test_filters_by_project(self):
        request = self.request_factory.get('/possible-tasks/list/', {'project': '3'})
        request.user = mock.Mock(is_authenticated=True)
        view = PossibleTaskListView()
        view.request = request

        base_queryset = mock.Mock()
        selected_queryset = mock.Mock()
        ordered_queryset = mock.Mock()
        project_filtered_queryset = mock.Mock()
        base_queryset.select_related.return_value = selected_queryset
        selected_queryset.order_by.return_value = ordered_queryset
        ordered_queryset.filter.return_value = project_filtered_queryset
        project_filtered_queryset.filter.return_value = project_filtered_queryset

        with patch.object(PossibleTask._default_manager, 'all', return_value=base_queryset):
            queryset = view.get_queryset()

        ordered_queryset.filter.assert_called_once_with(project_id='3')
        project_filtered_queryset.filter.assert_called_once_with(
            generated_task__isnull=True,
            generated_recurring_task__isnull=True,
            generated_project_task__isnull=True,
        )
        self.assertIs(queryset, project_filtered_queryset)

    def test_filters_by_unassigned_project(self):
        request = self.request_factory.get('/possible-tasks/list/', {'project': 'none'})
        request.user = mock.Mock(is_authenticated=True)
        view = PossibleTaskListView()
        view.request = request

        base_queryset = mock.Mock()
        selected_queryset = mock.Mock()
        ordered_queryset = mock.Mock()
        project_filtered_queryset = mock.Mock()
        base_queryset.select_related.return_value = selected_queryset
        selected_queryset.order_by.return_value = ordered_queryset
        ordered_queryset.filter.return_value = project_filtered_queryset
        project_filtered_queryset.filter.return_value = project_filtered_queryset

        with patch.object(PossibleTask._default_manager, 'all', return_value=base_queryset):
            queryset = view.get_queryset()

        ordered_queryset.filter.assert_called_once_with(project__isnull=True)
        project_filtered_queryset.filter.assert_called_once_with(
            generated_task__isnull=True,
            generated_recurring_task__isnull=True,
            generated_project_task__isnull=True,
        )
        self.assertIs(queryset, project_filtered_queryset)

    def test_filters_by_conversion_status(self):
        request = self.request_factory.get('/possible-tasks/list/', {'conversion': 'converted'})
        request.user = mock.Mock(is_authenticated=True)
        view = PossibleTaskListView()
        view.request = request

        base_queryset = mock.Mock()
        selected_queryset = mock.Mock()
        ordered_queryset = mock.Mock()
        filtered_queryset = mock.Mock()
        base_queryset.select_related.return_value = selected_queryset
        selected_queryset.order_by.return_value = ordered_queryset
        ordered_queryset.filter.return_value = filtered_queryset

        with patch.object(PossibleTask._default_manager, 'all', return_value=base_queryset):
            queryset = view.get_queryset()

        ordered_queryset.filter.assert_called_once()
        self.assertIs(queryset, filtered_queryset)

    def test_filters_by_not_converted_status(self):
        request = self.request_factory.get('/possible-tasks/list/', {'conversion': 'not_converted'})
        request.user = mock.Mock(is_authenticated=True)
        view = PossibleTaskListView()
        view.request = request

        base_queryset = mock.Mock()
        selected_queryset = mock.Mock()
        ordered_queryset = mock.Mock()
        default_filtered_queryset = mock.Mock()
        filtered_queryset = mock.Mock()
        base_queryset.select_related.return_value = selected_queryset
        selected_queryset.order_by.return_value = ordered_queryset
        ordered_queryset.filter.return_value = default_filtered_queryset
        default_filtered_queryset.filter.return_value = filtered_queryset

        with patch.object(PossibleTask._default_manager, 'all', return_value=base_queryset):
            queryset = view.get_queryset()

        ordered_queryset.filter.assert_called_once_with(
            generated_task__isnull=True,
            generated_recurring_task__isnull=True,
            generated_project_task__isnull=True,
        )

    def test_defaults_to_not_converted_when_conversion_is_missing(self):
        request = self.request_factory.get('/possible-tasks/list/')
        request.user = mock.Mock(is_authenticated=True)
        view = PossibleTaskListView()
        view.request = request

        base_queryset = mock.Mock()
        selected_queryset = mock.Mock()
        ordered_queryset = mock.Mock()
        filtered_queryset = mock.Mock()
        base_queryset.select_related.return_value = selected_queryset
        selected_queryset.order_by.return_value = ordered_queryset
        ordered_queryset.filter.return_value = filtered_queryset

        with patch.object(PossibleTask._default_manager, 'all', return_value=base_queryset):
            queryset = view.get_queryset()

        ordered_queryset.filter.assert_called_once_with(
            generated_task__isnull=True,
            generated_recurring_task__isnull=True,
            generated_project_task__isnull=True,
        )
        self.assertIs(queryset, filtered_queryset)


class PossibleTaskCreateViewTests(SimpleTestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

    def test_defaults_to_default_project_when_no_project_is_provided(self):
        request = self.request_factory.get('/possible-tasks/create/')
        request.user = mock.Mock(is_authenticated=True)
        view = PossibleTaskCreateView()
        view.request = request

        default_project = mock.Mock(pk=17)

        with patch('possible_tasks.views.project_services.get_default_project', return_value=default_project):
            initial = view.get_initial()

        self.assertEqual(initial['project'], 17)
