from datetime import timedelta

from django.db.models import Count, Q
from django.db.models.functions import ExtractIsoWeekDay
from django.utils import timezone

from tasks.models import Task
from tasks.services import filter_pending_tasks


WEEKDAY_LABELS = {
    1: 'Segunda-feira',
    2: 'Terça-feira',
    3: 'Quarta-feira',
    4: 'Quinta-feira',
    5: 'Sexta-feira',
    6: 'Sábado',
    7: 'Domingo',
}


def get_default_range(reference_date=None):
    reference_date = reference_date or timezone.localdate()
    return reference_date - timedelta(days=6), reference_date


def normalize_range(start_date=None, end_date=None, reference_date=None):
    default_start, default_end = get_default_range(reference_date=reference_date)
    return start_date or default_start, end_date or default_end


def get_today_summary(reference_date=None):
    reference_date = reference_date or timezone.localdate()
    queryset = Task.objects.filter(scheduled_date=reference_date)
    total = queryset.count()
    completed = queryset.filter(completed_at__isnull=False).count()
    pending = filter_pending_tasks(queryset).count()
    not_completed = queryset.filter(completed_at__isnull=True, skipped_in__isnull=False).count()
    completion_rate = int((completed / total) * 100) if total else 0

    return {
        'date': reference_date,
        'total': total,
        'completed': completed,
        'pending': pending,
        'not_completed': not_completed,
        'completion_rate': completion_rate,
    }


def build_weekday_productivity(rows):
    summary = [
        {
            'weekday': weekday,
            'label': WEEKDAY_LABELS[weekday],
            'total': 0,
            'completed': 0,
            'rate': 0,
        }
        for weekday in range(1, 8)
    ]

    by_weekday = {row['weekday']: row for row in rows}
    for item in summary:
        row = by_weekday.get(item['weekday'])
        if not row:
            continue
        item['total'] = row['total']
        item['completed'] = row['completed']
        item['rate'] = int((row['completed'] / row['total']) * 100) if row['total'] else 0

    return summary


def get_range_summary(start_date=None, end_date=None, reference_date=None):
    start_date, end_date = normalize_range(start_date, end_date)
    reference_date = reference_date or timezone.localdate()
    queryset = Task.objects.filter(scheduled_date__range=(start_date, end_date))

    total = queryset.count()
    completed = queryset.filter(completed_at__isnull=False).count()
    pending = filter_pending_tasks(queryset).count()
    not_completed = queryset.filter(
        (
            Q(completed_at__isnull=True, skipped_in__isnull=True, scheduled_date__lt=reference_date)
            | Q(skipped_in__isnull=False, scheduled_date__lte=reference_date)
        )
    ).count()
    completion_rate = int((completed / total) * 100) if total else 0

    weekday_rows = (
        queryset.annotate(weekday=ExtractIsoWeekDay('scheduled_date'))
        .values('weekday')
        .annotate(
            total=Count('id'),
            completed=Count('id', filter=Q(completed_at__isnull=False)),
        )
        .order_by('weekday')
    )

    pending_tasks = filter_pending_tasks(queryset).select_related('recurring_task', 'category')

    return {
        'start_date': start_date,
        'end_date': end_date,
        'total': total,
        'completed': completed,
        'not_completed': not_completed,
        'pending': pending,
        'completion_rate': completion_rate,
        'weekday_productivity': build_weekday_productivity(list(weekday_rows)),
        'pending_tasks': pending_tasks,
    }


def get_dashboard_context(start_date=None, end_date=None, reference_date=None):
    reference_date = reference_date or timezone.localdate()
    today_summary = get_today_summary(reference_date=reference_date)
    range_summary = get_range_summary(start_date, end_date, reference_date=reference_date)

    return {
        'today_summary': today_summary,
        'range_summary': range_summary,
        'completion_chart_data': {
            'labels': ['Concluídas', 'Pendentes', 'Não concluídas'],
            'values': [today_summary['completed'], today_summary['pending'], today_summary['not_completed']],
        },
        'range_status_chart_data': {
            'labels': ['Concluídas', 'Pendentes abertas', 'Não concluídas'],
            'values': [range_summary['completed'], range_summary['pending'], range_summary['not_completed']],
        },
        'weekday_chart_data': {
            'labels': [item['label'] for item in range_summary['weekday_productivity']],
            'values': [item['rate'] for item in range_summary['weekday_productivity']],
        },
    }
