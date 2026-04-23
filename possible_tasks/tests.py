from django.test import SimpleTestCase
from django.urls import reverse

from .models import PossibleTask


class PossibleTaskModelTests(SimpleTestCase):
    def test_str_returns_title(self):
        task = PossibleTask(title='Organizar estação', description='Organizar mesa de trabalho')

        self.assertEqual(str(task), 'Organizar estação')

    def test_defaults_to_low_priority(self):
        task = PossibleTask(title='Organizar estação', description='Organizar mesa de trabalho')

        self.assertEqual(task.priority, PossibleTask.Priority.LOW)


class PossibleTaskUrlTests(SimpleTestCase):
    def test_list_urls_exist(self):
        self.assertEqual(reverse('possible_task_list'), '/possible-tasks/list/')
        self.assertEqual(reverse('possible_task_create'), '/possible-tasks/create/')
        self.assertEqual(reverse('possible_task_update', args=[1]), '/possible-tasks/1/update/')
        self.assertEqual(reverse('possible_task_delete', args=[1]), '/possible-tasks/1/delete/')
