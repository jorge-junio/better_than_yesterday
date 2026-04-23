from unittest.mock import patch

from django.test import SimpleTestCase, TestCase

from projects.models import Project

from .models import ProjectTask
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


class ProjectTaskServiceTests(TestCase):
    def test_complete_project_task_sets_percentage_to_100(self):
        project = Project(title='Website', description='Novo site institucional')
        task = ProjectTask(
            project=project,
            title='Criar home',
            description='Montar a página inicial',
        )

        with patch.object(ProjectTask, 'save') as save_mock:
            complete_project_task(task)

        self.assertEqual(task.status, ProjectTask.Status.COMPLETED)
        self.assertEqual(task.completion_percentage, 100)
        self.assertIsNotNone(task.completed_at)
        save_mock.assert_called_once()
