from datetime import date

from django.test import SimpleTestCase

from . import forms, services


class ProgressFormTests(SimpleTestCase):
    def test_dashboard_filter_rejects_invalid_range(self):
        form = forms.DashboardFilterForm(data={
            'start_date': '2026-04-22',
            'end_date': '2026-04-21',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('A data final deve ser maior ou igual à data inicial.', str(form.errors))


class ProgressServiceTests(SimpleTestCase):
    def test_default_range_uses_last_seven_days(self):
        start_date, end_date = services.get_default_range(reference_date=date(2026, 4, 22))

        self.assertEqual(start_date.isoformat(), '2026-04-16')
        self.assertEqual(end_date.isoformat(), '2026-04-22')

    def test_weekday_productivity_fills_missing_days(self):
        rows = [
            {'weekday': 3, 'total': 4, 'completed': 3},
        ]

        summary = services.build_weekday_productivity(rows)

        self.assertEqual(len(summary), 7)
        self.assertEqual(summary[2]['total'], 4)
        self.assertEqual(summary[2]['rate'], 75)
