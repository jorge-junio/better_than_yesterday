from django.contrib import admin

from .models import ProjectTask


@admin.register(ProjectTask)
class ProjectTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'project', 'priority', 'status', 'completion_percentage', 'completed_at')
    list_filter = ('project', 'priority', 'status')
    search_fields = ('title', 'description', 'project__title')
