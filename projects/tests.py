from unittest import mock
from contextlib import nullcontext

from django.test import RequestFactory, SimpleTestCase

from .models import Project
from .services import get_default_project
from .views import ProjectListView


class ProjectModelTests(SimpleTestCase):
    def test_str_returns_title(self):
        project = Project(title='Website', description='Novo site institucional')

        self.assertEqual(str(project), 'Website')

    def test_default_flag_exists_and_defaults_to_false(self):
        field = Project._meta.get_field('is_default')

        self.assertFalse(field.default)
        self.assertFalse(Project(title='Website', description='Novo site institucional').is_default)


class ProjectModelSaveTests(SimpleTestCase):
    def test_saving_one_default_clears_the_others(self):
        project = Project(title='Alpha', description='Primeiro projeto', is_default=True)

        with mock.patch.object(Project.objects, 'filter') as filter_mock, mock.patch(
            'projects.models.transaction.atomic',
            return_value=nullcontext(),
        ), mock.patch('projects.models.models.Model.save') as base_save:
            filter_mock.return_value.exclude.return_value.update.return_value = 1
            project.save()

        filter_mock.assert_called_once_with(is_default=True)
        filter_mock.return_value.exclude.assert_called_once_with(pk=None)
        filter_mock.return_value.exclude.return_value.update.assert_called_once_with(is_default=False)
        base_save.assert_called_once()

    def test_get_default_project_returns_the_default_project(self):
        expected = Project(title='Beta', description='Segundo projeto', is_default=True)

        with mock.patch.object(Project.objects, 'filter') as filter_mock:
            filter_mock.return_value.order_by.return_value.first.return_value = expected

            self.assertEqual(get_default_project(), expected)
            filter_mock.assert_called_once_with(is_default=True)
            filter_mock.return_value.order_by.assert_called_once_with('id')


class ProjectListViewTests(SimpleTestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

    def test_filters_projects_by_title(self):
        request = self.request_factory.get('/projects/list/', {'title': 'Web'})
        request.user = mock.Mock(is_authenticated=True)
        view = ProjectListView()
        view.request = request

        fake_queryset = mock.Mock()
        with mock.patch.object(Project._default_manager, 'all', return_value=fake_queryset):
            queryset = view.get_queryset()

        fake_queryset.filter.assert_called_once_with(title__icontains='Web')
        self.assertIs(queryset, fake_queryset.filter.return_value)
