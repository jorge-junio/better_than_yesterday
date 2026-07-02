from django import forms

from projects.models import Project

from . import models


class PossibleTaskForm(forms.ModelForm):
    project = forms.ModelChoiceField(
        queryset=Project.objects.order_by('title'),
        required=False,
        empty_label='Sem projeto',
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Projeto',
    )

    class Meta:
        model = models.PossibleTask
        fields = ['title', 'description', 'project', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'title': 'Título',
            'description': 'O que precisa ser feito',
            'project': 'Projeto',
            'priority': 'Prioridade',
        }
