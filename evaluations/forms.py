from django import forms

from . import models
from .services import get_quizable_words_count


class EvaluationForm(forms.ModelForm):
    class Meta:
        model = models.Evaluation
        fields = ['questions_requested']
        widgets = {
            'questions_requested': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
        labels = {
            'questions_requested': 'Quantidade de perguntas',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        max_questions = get_quizable_words_count()
        field = self.fields['questions_requested']
        field.max_value = max_questions
        field.help_text = f'Máximo disponível hoje: {max_questions}.'

    def clean_questions_requested(self):
        requested = self.cleaned_data['questions_requested']
        max_questions = get_quizable_words_count()
        if requested > max_questions:
            raise forms.ValidationError(f'O máximo atual é {max_questions} pergunta(s).')
        if (
            self.instance
            and self.instance.pk
            and (self.instance.quiz_word_ids or self.instance.items.exists())
            and requested != self.instance.questions_requested
        ):
            raise forms.ValidationError('Não é possível alterar a quantidade depois que o quiz foi iniciado.')
        return requested


class EvaluationAnswerForm(forms.Form):
    answer = forms.CharField(
        label='Minha resposta',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg text-uppercase',
            'data-uppercase': 'true',
            'placeholder': 'Digite a tradução',
            'autocomplete': 'off',
            'autofocus': True,
        }),
    )

    def clean_answer(self):
        return self.cleaned_data['answer'].strip().upper()


class EvaluationItemForm(forms.ModelForm):
    class Meta:
        model = models.EvaluationItem
        fields = ['word', 'answer', 'is_correct']
        widgets = {
            'word': forms.Select(attrs={'class': 'form-select'}),
            'answer': forms.Textarea(attrs={'class': 'form-control text-uppercase', 'rows': 3, 'data-uppercase': 'true'}),
            'is_correct': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'word': 'Palavra',
            'answer': 'Minha resposta',
            'is_correct': 'Acertou',
        }

    def clean_answer(self):
        return self.cleaned_data.get('answer', '').strip().upper()
