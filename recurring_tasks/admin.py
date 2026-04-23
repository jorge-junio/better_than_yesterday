from django.contrib import admin

from . import models


@admin.register(models.RecurringTask)
class RecurringTaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'estimated_time', 'task_type', 'recurrence_type', 'is_active', 'created_at')
    list_filter = ('task_type', 'recurrence_type', 'is_active')
    search_fields = ('name', 'description')
    ordering = ('name',)
