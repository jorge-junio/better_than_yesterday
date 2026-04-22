from django.contrib import admin

from . import models


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'scheduled_date', 'scheduled_time', 'source_type', 'is_completed')
    list_filter = ('scheduled_date', 'source_type', 'is_completed')
    search_fields = ('title', 'description')
    ordering = ('-scheduled_date', 'scheduled_time', 'title')
