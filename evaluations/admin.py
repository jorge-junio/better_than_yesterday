from django.contrib import admin

from .forms import EvaluationItemForm
from .models import Evaluation, EvaluationItem


class EvaluationItemInline(admin.TabularInline):
    model = EvaluationItem
    form = EvaluationItemForm
    extra = 0


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('id', 'tested_at', 'questions_requested', 'max_questions', 'correct_items_count', 'incorrect_items_count')
    list_filter = ('tested_at',)
    inlines = [EvaluationItemInline]
