from django import forms

from . import models


class PossibleTaskForm(forms.ModelForm):
    class Meta:
        model = models.PossibleTask
        fields = ['title', 'description', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'title': 'Título',
            'description': 'O que precisa ser feito',
            'priority': 'Prioridade',
        }
