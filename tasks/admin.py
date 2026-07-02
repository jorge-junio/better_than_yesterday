from django.contrib import admin

from . import models


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'scheduled_date',
        'scheduled_time',
        'estimated_time',
        'priority',
        'source_type',
        'completed_at',
        'is_completed',
        'is_skipped',
    )
    list_filter = ('scheduled_date', 'category', 'priority', 'source_type', 'is_completed')
    search_fields = ('title', 'description')
    ordering = ('-scheduled_date', 'scheduled_time', 'title')
