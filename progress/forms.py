from datetime import timedelta

from django import forms
from django.utils import timezone


class DashboardFilterForm(forms.Form):
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='Data inicial',
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='Data final',
    )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError('A data final deve ser maior ou igual à data inicial.')

        return cleaned_data

    @staticmethod
    def default_range(reference_date=None):
        reference_date = reference_date or timezone.localdate()
        return reference_date - timedelta(days=6), reference_date
