from datetime import date
from unittest import mock

from django.db.models import Q
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

    def test_range_summary_exposes_not_completed_count(self):
        queryset = mock.Mock()
        completed_queryset = mock.Mock()
        pending_queryset = mock.Mock()
        not_completed_queryset = mock.Mock()
        annotated_queryset = mock.Mock()

        queryset.count.return_value = 5
        queryset.filter.side_effect = [
            completed_queryset,
            pending_queryset,
            not_completed_queryset,
            pending_queryset,
        ]
        queryset.annotate.return_value = annotated_queryset
        annotated_queryset.values.return_value = annotated_queryset
        annotated_queryset.annotate.return_value = annotated_queryset
        annotated_queryset.order_by.return_value = []
        pending_queryset.select_related.return_value = pending_queryset
        pending_queryset.count.return_value = 2
        completed_queryset.count.return_value = 3
        not_completed_queryset.count.return_value = 1

        with mock.patch('progress.services.Task.objects.filter', return_value=queryset), mock.patch('progress.services.timezone.localdate', return_value=date(2026, 4, 22)):
            summary = services.get_range_summary(
                start_date=date(2026, 4, 16),
                end_date=date(2026, 4, 22),
                reference_date=date(2026, 4, 22),
            )

        self.assertIn('not_completed', summary)
        queryset.filter.assert_any_call(
            completed_at__isnull=True,
            skipped_in__isnull=True,
            scheduled_date=date(2026, 4, 22),
        )
        queryset.filter.assert_any_call(
            Q(completed_at__isnull=True, skipped_in__isnull=True, scheduled_date__lt=date(2026, 4, 22))
            | Q(skipped_in__isnull=False, scheduled_date__lte=date(2026, 4, 22))
        )

    def test_dashboard_context_uses_three_range_status_segments(self):
        with mock.patch('progress.services.get_today_summary', return_value={
            'completed': 2,
            'pending': 1,
            'not_completed': 1,
            'completion_rate': 66,
        }), mock.patch('progress.services.get_range_summary', return_value={
            'start_date': date(2026, 4, 16),
            'end_date': date(2026, 4, 22),
            'total': 3,
            'completed': 1,
            'pending': 1,
            'not_completed': 1,
            'completion_rate': 33,
            'weekday_productivity': [{'label': 'Segunda-feira', 'rate': 0}] * 7,
            'pending_tasks': [],
        }) as range_mock, mock.patch('progress.services.timezone.localdate', return_value=date(2026, 4, 22)):
            context = services.get_dashboard_context(start_date=date(2026, 4, 16), end_date=date(2026, 4, 22), reference_date=date(2026, 4, 22))

        range_mock.assert_called_once_with(date(2026, 4, 16), date(2026, 4, 22), reference_date=date(2026, 4, 22))
        self.assertEqual(context['completion_chart_data']['labels'], ['Concluídas', 'Pendentes', 'Não concluídas'])
        self.assertEqual(context['completion_chart_data']['values'], [2, 1, 1])
        self.assertEqual(context['range_status_chart_data']['labels'], ['Concluídas', 'Pendentes abertas', 'Não concluídas'])
        self.assertEqual(context['range_status_chart_data']['values'], [1, 1, 1])
