from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True, verbose_name='nome')
    color = models.CharField(max_length=7, default='#0f766e', verbose_name='cor')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def color_style(self):
        return f'background-color: {self.color};'
