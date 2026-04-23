from django.test import SimpleTestCase

from .models import Project


class ProjectModelTests(SimpleTestCase):
    def test_str_returns_title(self):
        project = Project(title='Website', description='Novo site institucional')

        self.assertEqual(str(project), 'Website')
