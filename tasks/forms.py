from django import forms
from django.db import models as db_models

from categories.models import Category

from . import models


class TaskForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.order_by('name'),
        required=False,
        empty_label='Sem categoria',
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Categoria',
    )

    class Meta:
        model = models.Task
        fields = [
            'title',
            'description',
            'estimated_time',
            'scheduled_date',
            'scheduled_time',
            'priority',
            'category',
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
            'category': 'Categoria',
            'is_completed': 'Concluída',
        }


class TaskFilterForm(forms.Form):
    class StatusChoices(db_models.TextChoices):
        ALL = 'all', 'Todas'
        COMPLETED = 'completed', 'Concluídas'
        PENDING = 'pending', 'Pendentes'
        POSTPONED = 'postponed', 'Adiadas'

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
