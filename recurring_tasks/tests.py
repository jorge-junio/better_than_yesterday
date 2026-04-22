from datetime import date

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from .models import RecurringTask


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
