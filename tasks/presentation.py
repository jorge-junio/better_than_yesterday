"""Shared category selection and display counts for the daily mission screens."""
from urllib.parse import urlencode

from .forms import DailyCategoryFilterForm


def get_daily_category_context(mission, params):
    form = DailyCategoryFilterForm(params or None, categories=mission['today_categories'])
    tasks = mission['all_tasks']
    selected = ''
    if form.is_bound:
        if form.is_valid():
            selected = form.cleaned_data.get('category', '')
            if selected == 'none':
                tasks = tasks.filter(category__isnull=True)
            elif selected:
                tasks = tasks.filter(category_id=selected)
        else:
            tasks = tasks.none()

    active = tasks.filter(skipped_in__isnull=True)
    total = active.count()
    completed = active.filter(completed_at__isnull=False).count()
    summary = {
        **mission, 'total_tasks': total, 'completed_tasks': completed,
        'today_xp': completed * 15,
        'completion_rate': int(completed / total * 100) if total else 0,
    }
    return {
        'mission': summary, 'daily_category_form': form,
        'selected_category_id': selected,
        'daily_category_query': f"?{urlencode({'category': selected})}" if selected else '',
    }, tasks
