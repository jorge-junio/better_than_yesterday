from django import forms

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
            'is_completed',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'estimated_time': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'HH:MM:SS'}
            ),
            'scheduled_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'scheduled_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'is_completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'title': 'Título',
            'description': 'Descrição',
            'estimated_time': 'Tempo estimado',
            'scheduled_date': 'Data',
            'scheduled_time': 'Horário',
            'is_completed': 'Concluída',
        }


class TaskFilterForm(forms.Form):
    scheduled_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='Data',
    )
    show_completed = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Ver concluídas',
    )
