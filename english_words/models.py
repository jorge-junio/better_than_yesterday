from django.db import models


class EnglishWord(models.Model):
    word = models.CharField(max_length=120, verbose_name='palavra')
    note = models.TextField(blank=True, verbose_name='observação')

    class Meta:
        verbose_name = 'Palavra em inglês'
        verbose_name_plural = 'Palavras em inglês'
        ordering = ['word']

    def __str__(self):
        return self.word

    @property
    def meanings_text(self):
        return [meaning.text for meaning in self.meanings.order_by('id')]


class EnglishMeaning(models.Model):
    word = models.ForeignKey(
        EnglishWord,
        on_delete=models.CASCADE,
        related_name='meanings',
        verbose_name='palavra',
    )
    text = models.TextField(verbose_name='significado')

    class Meta:
        verbose_name = 'Significado'
        verbose_name_plural = 'Significados'
        ordering = ['id']

    def __str__(self):
        return self.text
