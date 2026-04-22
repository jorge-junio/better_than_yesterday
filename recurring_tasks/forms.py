from django import forms

from . import models


class RecurringTaskForm(forms.ModelForm):
    weekdays = forms.MultipleChoiceField(
        choices=models.RecurringTask.WEEKDAY_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Dias da semana',
    )
    specific_dates = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        label='Datas específicas',
        help_text='Informe uma data por linha no formato YYYY-MM-DD.',
    )

    class Meta:
        model = models.RecurringTask
        fields = [
            'name',
            'description',
            'recurrence_type',
            'weekdays',
            'start_date',
            'end_date',
            'specific_dates',
            'is_active',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'recurrence_type': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'name': 'Nome',
            'description': 'Descrição',
            'recurrence_type': 'Tipo de recorrência',
            'start_date': 'Data inicial',
            'end_date': 'Data final',
            'is_active': 'Ativo',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['weekdays'].initial = self.instance.weekdays
            self.fields['specific_dates'].initial = '\n'.join(self.instance.specific_dates)

    def clean_weekdays(self):
        weekdays = self.cleaned_data.get('weekdays') or []
        return list(weekdays)

    def clean_specific_dates(self):
        raw_value = self.cleaned_data.get('specific_dates') or ''
        if not raw_value.strip():
            return []

        dates = []
        for line in raw_value.replace(',', '\n').splitlines():
            candidate = line.strip()
            if candidate:
                try:
                    forms.DateField(input_formats=['%Y-%m-%d']).clean(candidate)
                except forms.ValidationError as exc:
                    raise forms.ValidationError(f'Data inválida: {candidate}') from exc
                dates.append(candidate)

        return dates

    def clean(self):
        cleaned_data = super().clean()
        recurrence_type = cleaned_data.get('recurrence_type')
        weekdays = cleaned_data.get('weekdays') or []
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        specific_dates = cleaned_data.get('specific_dates') or []

        if recurrence_type == models.RecurringTask.RecurrenceType.WEEKDAYS and not weekdays:
            self.add_error('weekdays', 'Selecione pelo menos um dia da semana.')

        if recurrence_type == models.RecurringTask.RecurrenceType.DATE_RANGE:
            if not start_date or not end_date:
                self.add_error('start_date', 'Informe a data inicial e a data final.')
            elif start_date > end_date:
                self.add_error('end_date', 'A data final deve ser maior ou igual à data inicial.')

        if recurrence_type == models.RecurringTask.RecurrenceType.SPECIFIC_DATES and not specific_dates:
            self.add_error('specific_dates', 'Informe ao menos uma data específica.')

        return cleaned_data
