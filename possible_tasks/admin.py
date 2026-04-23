from django.contrib import admin

from . import models


@admin.register(models.PossibleTask)
class PossibleTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
