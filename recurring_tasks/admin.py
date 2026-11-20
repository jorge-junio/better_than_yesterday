from django.contrib import admin

from . import models


@admin.register(models.RecurringTask)
class RecurringTaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'skill', 'estimated_time', 'priority', 'recurrence_type', 'is_active', 'created_at')
    list_filter = ('category', 'skill', 'priority', 'recurrence_type', 'is_active')
    search_fields = ('name', 'description')
    ordering = ('name',)
