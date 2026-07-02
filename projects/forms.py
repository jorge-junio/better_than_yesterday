from django import forms

from . import models


class ProjectForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = ['title', 'description', 'is_default']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'is_default': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'title': 'Título',
            'description': 'Descrição',
            'is_default': 'Projeto padrão',
        }
