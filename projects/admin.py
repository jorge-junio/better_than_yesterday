from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_default', 'created_at', 'updated_at')
    list_filter = ('is_default',)
    search_fields = ('title', 'description')
