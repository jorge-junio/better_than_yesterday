from unittest import mock
from unittest.mock import patch
from types import SimpleNamespace

from django.test import RequestFactory, SimpleTestCase

from projects.models import Project

from .models import ProjectTask
from .views import ProjectTaskCreateView, ProjectTaskListView
from .services import complete_project_task


class ProjectTaskModelTests(SimpleTestCase):
    def test_defaults_to_pending_and_low_priority(self):
        project = Project(title='Website', description='Novo site institucional')
        task = ProjectTask(
            project=project,
            title='Criar home',
            description='Montar a página inicial',
        )

        self.assertEqual(task.status, ProjectTask.Status.PENDING)
        self.assertEqual(task.priority, ProjectTask.Priority.LOW)
        self.assertFalse(task.is_completed)


class ProjectTaskServiceTests(SimpleTestCase):
    def test_complete_project_task_sets_percentage_to_100(self):
        project = Project(title='Website', description='Novo site institucional')
        task = ProjectTask(
            project=project,
            title='Criar home',
            description='Montar a página inicial',
        )

        with patch.object(ProjectTask, 'save') as save_mock, patch('project_tasks.services.timezone.now') as now_mock:
            now_mock.return_value = object()
            complete_project_task.__wrapped__(task)

        self.assertEqual(task.status, ProjectTask.Status.COMPLETED)
        self.assertEqual(task.completion_percentage, 100)
        self.assertIsNotNone(task.completed_at)
        save_mock.assert_called_once()


class ProjectTaskListViewTests(SimpleTestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

    def test_filters_by_project(self):
        request = self.request_factory.get('/project-tasks/list/', {'project': '7'})
        request.user = mock.Mock(is_authenticated=True)
        view = ProjectTaskListView()
        view.request = request

        base_queryset = mock.Mock()
        selected_queryset = mock.Mock()
        ordered_queryset = mock.Mock()
        base_queryset.select_related.return_value = selected_queryset
        selected_queryset.order_by.return_value = ordered_queryset

        with patch.object(ProjectTask._default_manager, 'all', return_value=base_queryset):
            queryset = view.get_queryset()

        ordered_queryset.filter.assert_called_once_with(project_id='7')
        self.assertIs(queryset, ordered_queryset.filter.return_value)

    def test_defaults_to_default_project_when_filter_is_missing(self):
        request = self.request_factory.get('/project-tasks/list/')
        request.user = mock.Mock(is_authenticated=True)
        view = ProjectTaskListView()
        view.request = request
        view.kwargs = {}

        base_queryset = mock.Mock()
        selected_queryset = mock.Mock()
        ordered_queryset = mock.Mock()
        filtered_queryset = mock.Mock()
        base_queryset.select_related.return_value = selected_queryset
        selected_queryset.order_by.return_value = ordered_queryset
        ordered_queryset.filter.return_value = filtered_queryset

        default_project = SimpleNamespace(id=11)

        with patch.object(ProjectTask._default_manager, 'all', return_value=base_queryset), patch(
            'project_tasks.views.project_services.get_default_project',
            return_value=default_project,
        ):
            queryset = view.get_queryset()

        ordered_queryset.filter.assert_called_once_with(project_id='11')
        self.assertIs(queryset, filtered_queryset)

    def test_shows_all_projects_when_filter_is_explicitly_empty(self):
        request = self.request_factory.get('/project-tasks/list/', {'project': ''})
        request.user = mock.Mock(is_authenticated=True)
        view = ProjectTaskListView()
        view.request = request
        view.kwargs = {}

        base_queryset = mock.Mock()
        selected_queryset = mock.Mock()
        ordered_queryset = mock.Mock()
        base_queryset.select_related.return_value = selected_queryset
        selected_queryset.order_by.return_value = ordered_queryset

        with patch.object(ProjectTask._default_manager, 'all', return_value=base_queryset), patch(
            'project_tasks.views.project_services.get_default_project'
        ) as default_project_mock:
            queryset = view.get_queryset()

        default_project_mock.assert_not_called()
        ordered_queryset.filter.assert_not_called()
        self.assertIs(queryset, ordered_queryset)

    def test_context_selects_default_project_when_filter_is_missing(self):
        request = self.request_factory.get('/project-tasks/list/')
        request.user = mock.Mock(is_authenticated=True)
        view = ProjectTaskListView()
        view.request = request
        view.kwargs = {}

        default_project = SimpleNamespace(id=11)

        with patch('project_tasks.views.project_services.get_default_project', return_value=default_project):
            context = view.get_context_data(object_list=[])

        self.assertEqual(context['selected_project_id'], '11')

    def test_context_leaves_selection_empty_when_filter_is_explicitly_empty(self):
        request = self.request_factory.get('/project-tasks/list/', {'project': ''})
        request.user = mock.Mock(is_authenticated=True)
        view = ProjectTaskListView()
        view.request = request
        view.kwargs = {}

        with patch('project_tasks.views.project_services.get_default_project') as default_project_mock:
            context = view.get_context_data(object_list=[])

        default_project_mock.assert_not_called()
        self.assertEqual(context['selected_project_id'], '')


class ProjectTaskCreateViewTests(SimpleTestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

    def test_prefills_possible_task_data(self):
        request = self.request_factory.get('/project-tasks/create/?possible_task=7')
        request.user = mock.Mock(is_authenticated=True)
        view = ProjectTaskCreateView()
        view.request = request

        possible_task = SimpleNamespace(
            title='Organizar campanha',
            description='Planejar a campanha do trimestre',
            priority=ProjectTask.Priority.HIGH,
            project_id='9',
        )

        with patch('project_tasks.views.possible_task_services.get_possible_task', return_value=possible_task):
            initial = view.get_initial()

        self.assertEqual(initial['title'], 'Organizar campanha')
        self.assertEqual(initial['description'], 'Planejar a campanha do trimestre')
        self.assertEqual(initial['priority'], ProjectTask.Priority.HIGH)
        self.assertEqual(initial['project'], '9')

    def test_defaults_to_default_project_when_no_project_is_provided(self):
        request = self.request_factory.get('/project-tasks/create/')
        request.user = mock.Mock(is_authenticated=True)
        view = ProjectTaskCreateView()
        view.request = request

        default_project = SimpleNamespace(pk=13)

        with patch('project_tasks.views.project_services.get_default_project', return_value=default_project):
            initial = view.get_initial()

        self.assertEqual(initial['project'], 13)
