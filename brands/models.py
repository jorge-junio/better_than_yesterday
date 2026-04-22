from django.db import models


class Brand(models.Model):

    name = models.CharField(max_length=500, verbose_name='nome')
    description = models.TextField(null=True, blank=True, verbose_name='descrição')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=['name'],
                name='brand_name_uk'
            )
        ]

    def __str__(self):
        return self.name
