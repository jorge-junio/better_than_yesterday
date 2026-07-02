from django.core.exceptions import ValidationError
from django.db import models

from english_words.models import EnglishWord

from .services import get_quizable_words_count


class Evaluation(models.Model):
    tested_at = models.DateTimeField(auto_now_add=True, verbose_name='avaliada em')
    questions_requested = models.PositiveSmallIntegerField(verbose_name='quantidade de perguntas')
    quiz_word_ids = models.JSONField(default=list, blank=True, editable=False, verbose_name='ordem das palavras')

    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'
        ordering = ['-tested_at']

    def __str__(self):
        return f'Avaliação de {self.tested_at:%Y-%m-%d %H:%M}' if self.tested_at else 'Avaliação'

    def clean(self):
        super().clean()
        max_questions = get_quizable_words_count()
        if self.questions_requested and self.questions_requested > max_questions:
            raise ValidationError({
                'questions_requested': f'O máximo atual é {max_questions} pergunta(s).',
            })

    def _get_items_cache(self):
        cache_attr = '_evaluation_items_cache'
        cached_items = getattr(self, cache_attr, None)
        if cached_items is not None:
            return cached_items

        prefetched_objects = getattr(self, '_prefetched_objects_cache', {})
        if 'items' in prefetched_objects:
            items = list(prefetched_objects['items'])
        elif self.pk:
            items = list(self.items.all())
        else:
            items = []

        setattr(self, cache_attr, items)
        return items

    def invalidate_items_cache(self):
        if hasattr(self, '_evaluation_items_cache'):
            delattr(self, '_evaluation_items_cache')
        prefetched_objects = getattr(self, '_prefetched_objects_cache', None)
        if prefetched_objects and 'items' in prefetched_objects:
            prefetched_objects.pop('items', None)

    @property
    def max_questions(self):
        return get_quizable_words_count()

    @property
    def answered_items_count(self):
        return len(self._get_items_cache())

    @property
    def pending_items_count(self):
        return max(self.questions_requested - self.answered_items_count, 0)

    @property
    def is_completed(self):
        return self.questions_requested > 0 and self.pending_items_count == 0

    @property
    def progress_percentage(self):
        if not self.questions_requested:
            return 0
        return min(100, round((self.answered_items_count / self.questions_requested) * 100))

    @property
    def correct_items_count(self):
        return sum(1 for item in self._get_items_cache() if item.is_correct)

    @property
    def incorrect_items_count(self):
        return sum(1 for item in self._get_items_cache() if not item.is_correct)


class EvaluationItem(models.Model):
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name='items', verbose_name='avaliação')
    word = models.ForeignKey(EnglishWord, on_delete=models.PROTECT, related_name='evaluation_items', verbose_name='palavra')
    answer = models.TextField(verbose_name='minha resposta')
    is_correct = models.BooleanField(default=False, verbose_name='acertou')

    class Meta:
        verbose_name = 'Item de avaliação'
        verbose_name_plural = 'Itens de avaliação'
        ordering = ['id']

    def __str__(self):
        return f'{self.word} - {"Acertou" if self.is_correct else "Errou"}'
