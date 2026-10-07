from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone

from . import models


def lock_owner(owner):
    get_user_model().objects.select_for_update().get(pk=owner.pk)


@transaction.atomic
def start_session(owner, list_id, item_ids):
    lock_owner(owner)
    existing = models.ShoppingSession.objects.filter(owner=owner, status=models.ShoppingSession.Status.IN_PROGRESS).first()
    if existing:
        return existing
    shopping_list = get_object_or_404(models.ShoppingList.objects.select_for_update(), pk=list_id, owner=owner, is_active=True)
    item_ids = set(item_ids)
    items = list(shopping_list.items.select_for_update().filter(pk__in=item_ids, is_active=True))
    if not items or len(items) != len(item_ids):
        raise ValidationError('Selecione itens ativos desta lista. O cadastro pode ter sido alterado; atualize a seleção.')
    session = models.ShoppingSession.objects.create(owner=owner, shopping_list=shopping_list, list_name=shopping_list.name)
    models.ShoppingSessionItem.objects.bulk_create([
        models.ShoppingSessionItem(session=session, source_item=item, name=item.name) for item in items
    ])
    return session


@transaction.atomic
def save_quantities(owner, session_id, quantities):
    session = get_object_or_404(models.ShoppingSession.objects.select_for_update(), pk=session_id, owner=owner)
    if session.status != models.ShoppingSession.Status.IN_PROGRESS:
        raise ValidationError('Esta compra já foi encerrada e não pode ser alterada.')
    items = list(session.items.select_for_update())
    if set(quantities) != {item.pk for item in items}:
        raise ValidationError('Os itens da compra foram alterados. Atualize a página.')
    for item in items:
        item.quantity = quantities[item.pk]
        item.full_clean()
    models.ShoppingSessionItem.objects.bulk_update(items, ['quantity'])
    return session


def validate_ready(session):
    quantities = list(session.items.values_list('quantity', flat=True))
    if not quantities or any(quantity is None for quantity in quantities):
        raise ValidationError('Informe a quantidade de todos os itens. Use 0 para um item que não foi comprado.')
    if not any(quantity > 0 for quantity in quantities):
        raise ValidationError('Informe uma quantidade maior que zero para pelo menos um item.')


@transaction.atomic
def finish_session(owner, session_id, total):
    session = get_object_or_404(models.ShoppingSession.objects.select_for_update(), pk=session_id, owner=owner)
    if session.status == models.ShoppingSession.Status.COMPLETED:
        return session
    if session.status != models.ShoppingSession.Status.IN_PROGRESS:
        raise ValidationError('Esta compra foi cancelada.')
    validate_ready(session)
    session.total = total
    session.status = models.ShoppingSession.Status.COMPLETED
    session.finished_at = timezone.now()
    session.full_clean()
    session.save(update_fields=['total', 'status', 'finished_at'])
    return session


@transaction.atomic
def cancel_session(owner, session_id):
    session = get_object_or_404(models.ShoppingSession.objects.select_for_update(), pk=session_id, owner=owner)
    if session.status == models.ShoppingSession.Status.IN_PROGRESS:
        session.status = models.ShoppingSession.Status.CANCELLED
        session.finished_at = timezone.now()
        session.save(update_fields=['status', 'finished_at'])
    return session
