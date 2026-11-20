from django import forms
from django.utils import timezone
from django.db import models as db_models

from categories.models import Category

from . import models


class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = [
            'title',
            'description',
            'estimated_time',
            'scheduled_date',
            'scheduled_time',
            'priority',
            'skill',
            'is_completed',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'estimated_time': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'HH:MM:SS'}
            ),
            'scheduled_date': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'scheduled_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'skill': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'is_completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'title': 'Título',
            'description': 'Descrição',
            'estimated_time': 'Tempo estimado',
            'scheduled_date': 'Data',
            'scheduled_time': 'Horário',
            'priority': 'Prioridade',
            'is_completed': 'Concluída',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['skill'].required = True
        self.fields['skill'].choices = [('', 'Selecione uma skill')] + list(models.Task.Skill.choices)

    def save(self, commit=True):
        task = super().save(commit=False)
        # Form completion and quick completion must use the same source of truth.
        if task.is_completed:
            task.completed_at = task.completed_at or timezone.now()
            task.skipped_in = None
        else:
            task.completed_at = None
        if commit:
            task.save()
            self.save_m2m()
        return task


class TaskFilterForm(forms.Form):
    class StatusChoices(db_models.TextChoices):
        ALL = 'all', 'Todas'
        COMPLETED = 'completed', 'Concluídas'
        PENDING = 'pending', 'Pendentes'
        POSTPONED = 'postponed', 'Adiadas'

    title = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Título',
    )
    description = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Descrição',
    )
    scheduled_date = forms.DateField(
        required=False,
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
        label='Data',
    )
    status = forms.ChoiceField(
        required=False,
        choices=StatusChoices.choices,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Status',
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.order_by('name'),
        required=False,
        empty_label='Todas as categorias',
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Categoria',
    )


class DailyCategoryFilterForm(forms.Form):
    skill = forms.ChoiceField(
        label='Skill', required=False,
        choices=[('', 'Todas as skills'), ('none', 'Sem skill')] + list(models.Task.Skill.choices),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    category = forms.ChoiceField(
        label='Categoria', required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    def __init__(self, *args, categories, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].choices = [
            ('', 'Todas as categorias'), ('none', 'Sem categoria'),
        ] + [(str(category.pk), category.name) for category in categories]
