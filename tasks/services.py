from datetime import timedelta

from django.db import transaction
from django.db.models import F
from django.utils import timezone

from categories.models import Category
from recurring_tasks.models import RecurringTask

from .models import Task


def ensure_tasks_for_date(target_date):
    recurring_tasks = RecurringTask.objects.filter(is_active=True)
    created = 0

    for recurring_task in recurring_tasks:
        if not recurring_task.occurs_on(target_date):
            continue

        _, was_created = Task.objects.get_or_create(
            scheduled_date=target_date,
            recurring_task=recurring_task,
            defaults={
                'title': recurring_task.name,
                'description': recurring_task.description,
                'estimated_time': recurring_task.estimated_time,
                'priority': recurring_task.priority,
                'category': recurring_task.category,
                'source_type': Task.SourceType.RECURRENT,
            },
        )
        if was_created:
            created += 1

    return created


@transaction.atomic
def start_task(task):
    now = timezone.now()
    if task.started_in is None:
        task.started_in = now
        task.save(update_fields=['started_in', 'updated_at'])
    return task


@transaction.atomic
def complete_task(task, time_spent=None, record_time_spent=True):
    started_now = False
    computed_time_spent = time_spent
    if task.is_skipped:
        task.skipped_in = None
    now = timezone.now()
    if task.started_in is None:
        task.started_in = now
        started_now = True

    if not task.is_completed:
        if computed_time_spent is None and record_time_spent:
            computed_time_spent = now - task.started_in if task.started_in is not None else timedelta(0)
        task.is_completed = True
        task.completed_at = now
        task.finished_in = now
        task.time_spent = computed_time_spent if record_time_spent else None
        update_fields = ['is_completed', 'completed_at', 'finished_in', 'time_spent', 'updated_at']
        if started_now:
            update_fields.append('started_in')
        if task.skipped_in is None:
            update_fields.append('skipped_in')
        task.save(update_fields=update_fields)
    return task


@transaction.atomic
def reopen_task(task):
    if task.is_completed:
        task.is_completed = False
        task.completed_at = None
        task.finished_in = None
        task.time_spent = None
        task.save(update_fields=['is_completed', 'completed_at', 'finished_in', 'time_spent', 'updated_at'])
    return task


@transaction.atomic
def skip_task_for_today(task):
    if not task.is_completed and task.skipped_in is None:
        task.skipped_in = timezone.now()
        task.save(update_fields=['skipped_in', 'updated_at'])
    return task


@transaction.atomic
def postpone_task(task, days=1):
    task.scheduled_date = task.scheduled_date + timedelta(days=days)
    task.save(update_fields=['scheduled_date', 'updated_at'])
    return task


def get_today_mission_ordering():
    return (
        F('started_in').desc(nulls_last=True),
        F('priority').desc(nulls_last=True),
        'title',
    )


def get_completion_streak(reference_date=None, lookback_days=60):
    reference_date = reference_date or timezone.localdate()
    streak = 0

    for offset in range(0, lookback_days):
        current_date = reference_date - timedelta(days=offset)
        day_tasks = Task.objects.filter(scheduled_date=current_date)
        total = day_tasks.count()

        if not total:
            if offset == 0:
                continue
            break

        completed = day_tasks.filter(is_completed=True).count()
        if completed != total:
            break

        streak += 1

    return streak


def get_today_mission_context(reference_date=None, category_id=None):
    reference_date = reference_date or timezone.localdate()
    ensure_tasks_for_date(reference_date)

    all_tasks = Task.objects.filter(scheduled_date=reference_date).select_related('recurring_task', 'category')
    active_tasks = all_tasks.filter(skipped_in__isnull=True)
    skipped_tasks = all_tasks.filter(skipped_in__isnull=False)
    pending_tasks = active_tasks.filter(is_completed=False)

    if category_id == 'none':
        pending_tasks = pending_tasks.filter(category__isnull=True)
    elif category_id:
        pending_tasks = pending_tasks.filter(category_id=category_id)

    pending_tasks = pending_tasks.order_by(*get_today_mission_ordering())
    total_tasks = active_tasks.count()
    completed_tasks = active_tasks.filter(is_completed=True).count()
    skipped_count = skipped_tasks.count()
    pending_count = total_tasks - completed_tasks
    visible_pending_count = pending_tasks.count()
    completion_rate = int((completed_tasks / total_tasks) * 100) if total_tasks else 0
    today_categories = Category.objects.filter(tasks__scheduled_date=reference_date).distinct().order_by('name')
    has_uncategorized_tasks = all_tasks.filter(category__isnull=True).exists()

    streak_days = get_completion_streak(reference_date=reference_date)
    lifetime_completed = Task.objects.filter(is_completed=True).count()
    total_xp = lifetime_completed * 15
    level = max(total_xp // 100 + 1, 1)
    xp_in_level = total_xp % 100
    xp_to_next_level = 100 - xp_in_level if xp_in_level else 100
    mission_complete = pending_count == 0

    badges = []
    if mission_complete:
        badges.append({
            'label': 'Missão concluída',
            'variant': 'success',
            'description': 'Você fechou todas as tarefas do dia.',
        })
    if streak_days >= 3:
        badges.append({
            'label': 'Sequência 3+',
            'variant': 'info',
            'description': 'Três dias seguidos com a agenda em dia.',
        })
    if streak_days >= 7:
        badges.append({
            'label': 'Sequência 7+',
            'variant': 'warning',
            'description': 'Uma semana de consistência.',
        })
    if completed_tasks >= 5:
        badges.append({
            'label': 'Ritmo forte',
            'variant': 'primary',
            'description': 'Cinco conclusões no dia são sinal de tração.',
        })
    if not badges:
        badges.append({
            'label': 'Primeiro passo',
            'variant': 'secondary',
            'description': 'Conclua uma tarefa para desbloquear seu primeiro selo.',
        })

    if level >= 6:
        rank_name = 'Lenda do foco'
    elif level >= 4:
        rank_name = 'Veterano disciplinado'
    elif level >= 3:
        rank_name = 'Ritmo constante'
    elif level >= 2:
        rank_name = 'Em evolução'
    else:
        rank_name = 'Recruta'

    return {
        'reference_date': reference_date,
        'all_tasks': all_tasks,
        'pending_tasks': pending_tasks,
        'today_categories': today_categories,
        'has_uncategorized_tasks': has_uncategorized_tasks,
        'selected_category_id': category_id or '',
        'visible_pending_count': visible_pending_count,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_count': pending_count,
        'skipped_count': skipped_count,
        'completion_rate': completion_rate,
        'streak_days': streak_days,
        'total_xp': total_xp,
        'level': level,
        'xp_in_level': xp_in_level,
        'xp_to_next_level': xp_to_next_level,
        'rank_name': rank_name,
        'mission_complete': mission_complete,
        'badges': badges,
        'today_xp': completed_tasks * 15,
    }
