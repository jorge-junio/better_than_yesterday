from django import forms

from . import models


class PossibleTaskForm(forms.ModelForm):
    class Meta:
        model = models.PossibleTask
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        labels = {
            'title': 'Título',
            'description': 'O que precisa ser feito',
        }
