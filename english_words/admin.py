from django.contrib import admin

from .models import EnglishMeaning, EnglishWord


class EnglishMeaningInline(admin.TabularInline):
    model = EnglishMeaning
    extra = 1


@admin.register(EnglishWord)
class EnglishWordAdmin(admin.ModelAdmin):
    list_display = ('id', 'word')
    search_fields = ('word', 'note', 'meanings__text')
    inlines = [EnglishMeaningInline]
