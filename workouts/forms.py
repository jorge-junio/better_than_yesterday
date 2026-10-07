import uuid
from django import forms
from django.utils import timezone
from .models import Exercise, Workout, WorkoutExercise, WorkoutSession, SessionSet, WEEKDAYS


class WorkoutForm(forms.ModelForm):
    confirm_activation = forms.BooleanField(required=False, label='Confirmo a substituição do treino ativo', widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    class Meta:
        model = Workout
        fields = ['name', 'start_date', 'end_date', 'rest_seconds', 'is_active']
        labels = {'name': 'Nome do treino', 'start_date': 'Data de início', 'end_date': 'Data final', 'is_active': 'Ativo'}
        help_texts = {
            'end_date': 'Opcional. Deixe em branco enquanto o treino não tiver uma data de encerramento.',
            'rest_seconds': 'Tempo entre séries, de 0 a 3.600 segundos. Use 0 para desativar a contagem regressiva.',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'rest_seconds': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 3600, 'inputmode': 'numeric'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, owner, **kwargs):
        super().__init__(*args, **kwargs)
        self.owner = owner
        self.other_active = Workout.objects.filter(owner=owner, is_active=True).exclude(pk=self.instance.pk).first()
        if self.other_active:
            self.fields['confirm_activation'].help_text = f'Ativar este treino desativará “{self.other_active.name}”.'
        else:
            self.fields['confirm_activation'].widget = forms.HiddenInput()

    def clean(self):
        data = super().clean()
        if data.get('is_active') and self.other_active and not data.get('confirm_activation'):
            self.add_error('confirm_activation', 'Confirme a substituição do treino ativo.')
        return data


class WorkoutExerciseForm(forms.ModelForm):
    exercise = forms.ModelChoiceField(queryset=Exercise.objects.none(), required=False, label='Exercício cadastrado', empty_label='Selecione ou cadastre abaixo', widget=forms.Select(attrs={'class': 'form-select'}))
    new_exercise_name = forms.CharField(required=False, max_length=160, label='Nome de um novo exercício', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: Supino reto'}))

    class Meta:
        model = WorkoutExercise
        fields = ['weekday', 'exercise', 'position', 'sets_count', 'repetitions', 'notes']
        labels = {'weekday': 'Dia da semana', 'position': 'Ordem de execução', 'sets_count': 'Quantidade de séries', 'repetitions': 'Repetições por série', 'notes': 'Observações'}
        widgets = {
            'weekday': forms.Select(attrs={'class': 'form-select'}),
            'position': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'sets_count': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 100}),
            'repetitions': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 1000}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, owner, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['exercise'].queryset = Exercise.objects.filter(owner=owner)
        self.order_fields(['weekday', 'exercise', 'new_exercise_name', 'position', 'sets_count', 'repetitions', 'notes'])

    def clean(self):
        data = super().clean()
        name = ' '.join((data.get('new_exercise_name') or '').split())
        data['new_exercise_name'] = name
        if not data.get('exercise') and not name:
            self.add_error('exercise', 'Selecione um exercício ou informe o nome de um novo.')
        if data.get('exercise') and name:
            self.add_error('new_exercise_name', 'Selecione um exercício existente ou crie um novo; use apenas uma opção.')
        return data

    def _get_validation_exclusions(self):
        exclusions = super()._get_validation_exclusions()
        # A new library exercise is resolved atomically by the service after validation.
        if not self.cleaned_data.get('exercise'):
            exclusions.add('exercise')
        return exclusions


class CopyWorkoutDayForm(forms.Form):
    destination_weekday = forms.TypedChoiceField(
        label='Copiar para', coerce=int,
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text='Os exercícios serão acrescentados ao final do dia escolhido. Os exercícios existentes serão preservados.',
    )

    def __init__(self, *args, source_weekday, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['destination_weekday'].choices = [('', 'Selecione o dia de destino')] + [
            (number, label) for number, label in WEEKDAYS if number != source_weekday
        ]


class StartSessionForm(forms.Form):
    weekday = forms.TypedChoiceField(label='Programação do dia', choices=WEEKDAYS, coerce=int, widget=forms.Select(attrs={'class': 'form-select'}))
    request_id = forms.UUIDField(widget=forms.HiddenInput(), initial=uuid.uuid4)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['weekday'].initial = timezone.localdate().weekday()


class SessionSetForm(forms.ModelForm):
    class Meta:
        model = SessionSet
        fields = ['repetitions', 'weight']
        labels = {'repetitions': 'Repetições realizadas', 'weight': 'Peso (kg)'}
        widgets = {
            'repetitions': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 1000, 'inputmode': 'numeric'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': '0.01', 'inputmode': 'decimal'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True

    def _get_validation_exclusions(self):
        # registered_at is set by the service when the complete record is saved.
        return super()._get_validation_exclusions() | {'registered_at'}


class HistoryFilterForm(forms.Form):
    start_date = forms.DateField(required=False, label='De', widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    end_date = forms.DateField(required=False, label='Até', widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    workout = forms.ModelChoiceField(queryset=Workout.objects.none(), required=False, label='Treino', widget=forms.Select(attrs={'class': 'form-select'}))
    exercise = forms.ModelChoiceField(queryset=Exercise.objects.none(), required=False, label='Exercício', widget=forms.Select(attrs={'class': 'form-select'}))
    status = forms.ChoiceField(required=False, label='Situação', choices=[('', 'Todas'), *WorkoutSession.Status.choices], widget=forms.Select(attrs={'class': 'form-select'}))

    def __init__(self, *args, owner, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['workout'].queryset = Workout.objects.filter(owner=owner)
        self.fields['exercise'].queryset = Exercise.objects.filter(owner=owner)

    def clean(self):
        data = super().clean()
        if data.get('start_date') and data.get('end_date') and data['end_date'] < data['start_date']:
            raise forms.ValidationError('A data final do filtro deve ser igual ou posterior à inicial.')
        return data
