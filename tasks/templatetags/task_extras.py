from datetime import timedelta

from django import template

register = template.Library()


@register.filter
def duration_hms(value):
    if not value:
        return ''

    if not isinstance(value, timedelta):
        return str(value)

    total_seconds = int(value.total_seconds())
    sign = '-' if total_seconds < 0 else ''
    total_seconds = abs(total_seconds)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f'{sign}{hours:02d}:{minutes:02d}:{seconds:02d}'


@register.filter
def duration_part(value, part):
    if not isinstance(value, timedelta):
        return 0

    total_seconds = abs(int(value.total_seconds()))
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    parts = {
        'hours': hours,
        'minutes': minutes,
        'seconds': seconds,
    }
    return parts.get(part, 0)
