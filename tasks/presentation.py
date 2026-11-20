"""Shared category/skill selection and display counts for the daily mission screens."""
from urllib.parse import urlencode

from .forms import DailyCategoryFilterForm


def get_daily_category_context(mission, params):
    form = DailyCategoryFilterForm(params or None, categories=mission['today_categories'])
    tasks = mission['all_tasks']
    selected = ''
    selected_skill = ''
    if form.is_bound:
        if form.is_valid():
            selected = form.cleaned_data.get('category', '')
            if selected == 'none':
                tasks = tasks.filter(category__isnull=True)
            elif selected:
                tasks = tasks.filter(category_id=selected)
            selected_skill = form.cleaned_data.get('skill', '')
            if selected_skill == 'none':
                tasks = tasks.filter(skill='')
            elif selected_skill:
                tasks = tasks.filter(skill=selected_skill)
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
    filters = {key: value for key, value in {'category': selected, 'skill': selected_skill}.items() if value}
    return {
        'mission': summary, 'daily_category_form': form,
        'selected_category_id': selected, 'selected_skill': selected_skill,
        'daily_category_query': f"?{urlencode(filters)}" if filters else '',
    }, tasks
