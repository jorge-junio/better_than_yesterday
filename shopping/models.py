from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.functions import Lower


class ShoppingList(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shopping_lists')
    name = models.CharField('Nome', max_length=160)
    created_at = models.DateTimeField('Data de criação', auto_now_add=True)
    is_active = models.BooleanField('Ativa', default=True)

    class Meta:
        ordering = ['name', 'id']
        verbose_name = 'Lista de compras'
        verbose_name_plural = 'Listas de compras'

    def __str__(self):
        return self.name


class ShoppingItem(models.Model):
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE, related_name='items')
    name = models.CharField('Nome', max_length=160)
    is_active = models.BooleanField('Ativo', default=True)

    class Meta:
        ordering = ['name', 'id']
        verbose_name = 'Item da feira'
        verbose_name_plural = 'Itens da feira'
        constraints = [models.UniqueConstraint(Lower('name'), 'shopping_list', name='shopping_unique_item_name')]

    def __str__(self):
        return self.name


class ShoppingSession(models.Model):
    class Status(models.TextChoices):
        IN_PROGRESS = 'in_progress', 'Em andamento'
        COMPLETED = 'completed', 'Concluída'
        CANCELLED = 'cancelled', 'Cancelada'

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shopping_sessions')
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.SET_NULL, null=True, blank=True, related_name='sessions')
    list_name = models.CharField('Lista', max_length=160)
    started_at = models.DateTimeField('Iniciada em', auto_now_add=True)
    finished_at = models.DateTimeField('Finalizada em', null=True, blank=True)
    status = models.CharField('Situação', max_length=16, choices=Status.choices, default=Status.IN_PROGRESS)
    total = models.DecimalField('Valor total (R$)', max_digits=12, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(Decimal('0'))])

    class Meta:
        ordering = ['-started_at', '-id']
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
        constraints = [
            models.UniqueConstraint(fields=['owner'], condition=models.Q(status='in_progress'), name='shopping_one_open_session'),
            models.CheckConstraint(condition=models.Q(total__isnull=True) | models.Q(total__gte=0), name='shopping_nonnegative_total'),
            models.CheckConstraint(
                condition=(models.Q(status='in_progress', finished_at__isnull=True, total__isnull=True) | models.Q(status='completed', finished_at__isnull=False, total__isnull=False) | models.Q(status='cancelled', finished_at__isnull=False, total__isnull=True)),
                name='shopping_valid_session_state',
            ),
        ]

    def __str__(self):
        return self.list_name


class ShoppingSessionItem(models.Model):
    session = models.ForeignKey(ShoppingSession, on_delete=models.CASCADE, related_name='items')
    source_item = models.ForeignKey(ShoppingItem, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField('Item', max_length=160)
    quantity = models.DecimalField('Quantidade', max_digits=9, decimal_places=3, null=True, blank=True, validators=[MinValueValidator(Decimal('0'))])

    class Meta:
        ordering = ['name', 'id']
        verbose_name = 'Item comprado'
        verbose_name_plural = 'Itens comprados'
        constraints = [models.CheckConstraint(condition=models.Q(quantity__isnull=True) | models.Q(quantity__gte=0), name='shopping_nonnegative_quantity')]
