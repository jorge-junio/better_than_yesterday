from django import forms

from . import models


class ProjectTaskForm(forms.ModelForm):
    class Meta:
        model = models.ProjectTask
        fields = ['project', 'title', 'description', 'priority', 'status', 'completion_percentage']
        widgets = {
            'project': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'completion_percentage': forms.NumberInput(
                attrs={'class': 'form-control', 'min': 0, 'max': 100}
            ),
        }
        labels = {
            'project': 'Projeto',
            'title': 'Título',
            'description': 'Descrição',
            'priority': 'Prioridade',
            'status': 'Status',
            'completion_percentage': 'Porcentagem de conclusão',
        }

    def clean_completion_percentage(self):
        value = self.cleaned_data.get('completion_percentage')
        if value is None:
            return 0
        return max(0, min(100, value))

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        completion_percentage = cleaned_data.get('completion_percentage')

        if status == models.ProjectTask.Status.COMPLETED or completion_percentage == 100:
            cleaned_data['status'] = models.ProjectTask.Status.COMPLETED
            cleaned_data['completion_percentage'] = 100
        elif completion_percentage is not None and completion_percentage < 100:
            cleaned_data['status'] = models.ProjectTask.Status.PENDING

        return cleaned_data
