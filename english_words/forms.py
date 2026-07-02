from django import forms

from . import models


class EnglishWordLookupForm(forms.Form):
    word = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={'class': 'form-control text-uppercase', 'data-uppercase': 'true'}),
        label='Palavra',
    )

    def clean_word(self):
        return self.cleaned_data['word'].strip().upper()


class EnglishWordEditorForm(forms.ModelForm):
    class Meta:
        model = models.EnglishWord
        fields = ['word', 'note']
        widgets = {
            'word': forms.TextInput(attrs={'class': 'form-control text-uppercase', 'readonly': 'readonly', 'data-uppercase': 'true'}),
            'note': forms.Textarea(attrs={'class': 'form-control text-uppercase', 'rows': 3, 'data-uppercase': 'true'}),
        }
        labels = {
            'word': 'Palavra',
            'note': 'Observação',
        }

    def __init__(self, *args, **kwargs):
        self.word_locked = kwargs.pop('word_locked', True)
        super().__init__(*args, **kwargs)
        if not self.word_locked:
            self.fields['word'].widget.attrs.pop('readonly', None)
        if self.instance and self.instance.pk:
            self.fields['word'].initial = self.instance.word

    def clean_word(self):
        if self.word_locked and self.instance.pk:
            return self.instance.word.strip().upper()
        return self.cleaned_data['word'].strip().upper()

    def clean_note(self):
        return self.cleaned_data.get('note', '').strip().upper()

    @staticmethod
    def normalize_meanings(values):
        return [value.strip().upper() for value in values if value and value.strip()]

    def save_meanings(self, instance, meanings):
        cleaned_meanings = self.normalize_meanings(meanings)
        instance.meanings.all().delete()
        models.EnglishMeaning.objects.bulk_create([
            models.EnglishMeaning(word=instance, text=meaning)
            for meaning in cleaned_meanings
        ])
        return instance
