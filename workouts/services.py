from collections import OrderedDict
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Count, Q, Sum, Max, F, DecimalField, ExpressionWrapper
from django.db.models.functions import TruncWeek, TruncMonth
from django.utils import timezone

from .models import Exercise, Workout, WorkoutExercise, WorkoutSession, SessionExercise, SessionSet, WEEKDAYS


def lock_owner(owner):
    return get_user_model().objects.select_for_update().get(pk=owner.pk)


@transaction.atomic
def save_workout(form, owner):
    lock_owner(owner)
    workout = Workout.objects.select_for_update().get(pk=form.instance.pk, owner=owner) if form.instance.pk else Workout(owner=owner)
    if workout.is_archived:
        raise ValidationError('Este treino foi arquivado. Restaure-o antes de editar.')
    if form.cleaned_data['is_active']:
        others = Workout.objects.filter(owner=owner, is_active=True).exclude(pk=workout.pk)
        if others.exists() and not form.cleaned_data.get('confirm_activation'):
            raise ValidationError('Outro treino está ativo. Confirme a substituição e salve novamente.')
        others.update(is_active=False)
    for name in ['name', 'start_date', 'end_date', 'rest_seconds', 'is_active']:
        setattr(workout, name, form.cleaned_data[name])
    workout.full_clean()
    workout.save()
    return workout


@transaction.atomic
def set_archived(workout_id, owner, archived):
    lock_owner(owner)
    workout = Workout.objects.select_for_update().get(pk=workout_id, owner=owner)
    workout.is_archived = archived
    if archived:
        workout.is_active = False
    workout.save(update_fields=['is_archived', 'is_active'])
    return workout


@transaction.atomic
def save_workout_exercise(form, workout_id, owner):
    lock_owner(owner)
    workout = Workout.objects.select_for_update().get(pk=workout_id, owner=owner)
    if workout.is_archived:
        raise ValidationError('Restaure o treino antes de alterar a programação.')
    entry = WorkoutExercise.objects.get(pk=form.instance.pk, workout=workout) if form.instance.pk else WorkoutExercise(workout=workout)
    exercise = form.cleaned_data['exercise']
    if exercise is None:
        name = form.cleaned_data['new_exercise_name']
        exercise = Exercise.objects.filter(owner=owner, name__iexact=name).first()
        if exercise is None:
            exercise = Exercise.objects.create(owner=owner, name=name)
    if exercise.owner_id != owner.pk:
        raise ValidationError('Exercício não disponível para este usuário.')
    entry.exercise = exercise
    for name in ['weekday', 'position', 'sets_count', 'repetitions', 'notes']:
        setattr(entry, name, form.cleaned_data[name])
    entry.full_clean()
    entry.save()
    return entry


@transaction.atomic
def copy_workout_day(workout_id, owner, source_weekday, destination_weekday):
    valid_days = dict(WEEKDAYS)
    if source_weekday not in valid_days or destination_weekday not in valid_days:
        raise ValidationError('Selecione um dia da semana válido.')
    if source_weekday == destination_weekday:
        raise ValidationError('O dia de destino deve ser diferente do dia de origem.')
    lock_owner(owner)
    workout = Workout.objects.select_for_update().get(pk=workout_id, owner=owner)
    if workout.is_archived:
        raise ValidationError('Restaure o treino antes de copiar a programação.')
    source = list(workout.exercises.filter(weekday=source_weekday).select_related('exercise'))
    if not source:
        raise ValidationError('O dia de origem não tem exercícios para copiar.')
    last_position = workout.exercises.filter(weekday=destination_weekday).aggregate(last=Max('position'))['last'] or 0
    copies = []
    for offset, entry in enumerate(source, start=1):
        copy = WorkoutExercise(
            workout=workout, exercise=entry.exercise, weekday=destination_weekday,
            position=last_position + offset, sets_count=entry.sets_count,
            repetitions=entry.repetitions, notes=entry.notes,
        )
        copy.full_clean()
        copies.append(copy)
    return WorkoutExercise.objects.bulk_create(copies)


@transaction.atomic
def remove_workout_exercise(entry_id, owner):
    lock_owner(owner)
    entry = WorkoutExercise.objects.select_related('workout').get(pk=entry_id, workout__owner=owner)
    Workout.objects.select_for_update().get(pk=entry.workout_id)
    if entry.workout.is_archived:
        raise ValidationError('Restaure o treino antes de alterar a programação.')
    entry.delete()


@transaction.atomic
def start_session(owner, weekday, request_id):
    # Serializing by owner also covers the first session, when no session row exists yet.
    lock_owner(owner)
    existing = WorkoutSession.objects.filter(owner=owner, request_id=request_id).first()
    if existing:
        return existing
    ongoing = WorkoutSession.objects.filter(owner=owner, status=WorkoutSession.Status.IN_PROGRESS).first()
    if ongoing:
        return ongoing
    today = timezone.localdate()
    workout = Workout.objects.select_for_update().filter(owner=owner, is_active=True, is_archived=False).first()
    if not workout:
        raise ValidationError('Ative um treino antes de iniciar uma sessão.')
    if not workout.is_valid_on(today):
        raise ValidationError('O treino ativo está fora do período de validade. Ajuste as datas antes de iniciar.')
    entries = list(workout.exercises.filter(weekday=weekday).select_related('exercise'))
    if not entries:
        raise ValidationError('Não há exercícios programados para este dia. Escolha outro dia ou edite o treino.')
    session = WorkoutSession.objects.create(owner=owner, workout=workout, workout_name=workout.name, rest_seconds=workout.rest_seconds, date=today, scheduled_weekday=weekday, request_id=request_id)
    for entry in entries:
        item = SessionExercise.objects.create(
            session=session, exercise=entry.exercise, exercise_name=entry.exercise.name,
            position=entry.position, target_sets=entry.sets_count,
            target_repetitions=entry.repetitions, notes=entry.notes,
        )
        SessionSet.objects.bulk_create([SessionSet(session_exercise=item, number=number) for number in range(1, entry.sets_count + 1)])
    return session


def lock_open_session(session_id, owner):
    session = WorkoutSession.objects.select_for_update().get(pk=session_id, owner=owner)
    if not session.is_open:
        raise ValidationError('Esta sessão já foi finalizada. Os registros não foram alterados.')
    return session


@transaction.atomic
def record_set(set_id, owner, repetitions, weight):
    item = SessionSet.objects.select_related('session_exercise').get(pk=set_id, session_exercise__session__owner=owner)
    lock_open_session(item.session_exercise.session_id, owner)
    # Reload after the session lock so a simultaneous skip or save cannot use stale state.
    item = SessionSet.objects.select_related('session_exercise').get(pk=set_id)
    if item.session_exercise.is_skipped:
        raise ValidationError('Retome o exercício antes de registrar uma série.')
    item.was_new_registration = item.registered_at is None
    item.repetitions = repetitions
    item.weight = weight
    item.registered_at = timezone.now()
    item.full_clean()
    item.save(update_fields=['repetitions', 'weight', 'registered_at'])
    return item


@transaction.atomic
def set_skipped(exercise_id, owner, skipped):
    item = SessionExercise.objects.get(pk=exercise_id, session__owner=owner)
    lock_open_session(item.session_id, owner)
    item.refresh_from_db()
    if skipped and item.sets.filter(registered_at__isnull=False).exists():
        raise ValidationError('Este exercício já tem séries registradas. Finalize a sessão como parcial para manter esses resultados.')
    item.is_skipped = skipped
    item.save(update_fields=['is_skipped'])
    return item


def session_progress(session):
    sets = SessionSet.objects.filter(session_exercise__session=session)
    total = sets.count()
    saved = sets.filter(registered_at__isnull=False).count()
    return {'total': total, 'saved': saved, 'remaining': total - saved, 'percentage': round(saved / total * 100) if total else 0}


@transaction.atomic
def finish_session(session_id, owner, confirm_partial=False):
    session = WorkoutSession.objects.select_for_update().get(pk=session_id, owner=owner)
    if not session.is_open:
        return session
    progress = session_progress(session)
    if progress['remaining'] and not confirm_partial:
        raise ValidationError('Há séries pendentes. Confirme a finalização parcial para manter os resultados já salvos.')
    session.status = WorkoutSession.Status.PARTIAL if progress['remaining'] else WorkoutSession.Status.COMPLETED
    session.finished_at = timezone.now()
    session.save(update_fields=['status', 'finished_at'])
    return session


def session_cards(session):
    items = list(session.exercises.select_related('exercise').prefetch_related('sets'))
    prior = SessionExercise.objects.filter(session__owner=session.owner, session__started_at__lt=session.started_at, sets__registered_at__isnull=False).exclude(session=session).prefetch_related('sets').order_by('exercise_id', '-session__started_at', '-pk')
    previous = {}
    exercise_ids = {item.exercise_id for item in items}
    for item in prior.filter(exercise_id__in=exercise_ids).distinct('exercise_id'):
        if item.exercise_id not in previous:
            previous[item.exercise_id] = item
    return [{'item': item, 'previous': previous.get(item.exercise_id)} for item in items]


def weekly_program(workout):
    grouped = OrderedDict((day, {'number': day, 'label': label, 'exercises': []}) for day, label in WEEKDAYS)
    for item in workout.exercises.select_related('exercise'):
        grouped[item.weekday]['exercises'].append(item)
    return list(grouped.values())


def filter_sessions(owner, data):
    queryset = WorkoutSession.objects.filter(owner=owner)
    for key, lookup in [('start_date', 'date__gte'), ('end_date', 'date__lte'), ('workout', 'workout'), ('status', 'status')]:
        if data.get(key):
            queryset = queryset.filter(**{lookup: data[key]})
    if data.get('exercise'):
        queryset = queryset.filter(pk__in=SessionExercise.objects.filter(exercise=data['exercise']).values('session_id'))
    return queryset


def annotate_sessions(queryset):
    return queryset.annotate(total_sets=Count('exercises__sets'), saved_sets=Count('exercises__sets', filter=Q(exercises__sets__registered_at__isnull=False))).order_by('-started_at', '-pk')


def build_reports(sessions, exercise=None):
    sets = SessionSet.objects.filter(session_exercise__session__in=sessions)
    summary = sessions.aggregate(total=Count('pk'), completed=Count('pk', filter=Q(status='completed')), partial=Count('pk', filter=Q(status='partial')), ongoing=Count('pk', filter=Q(status='in_progress')))
    summary['planned_sets'] = sets.count()
    summary['saved_sets'] = sets.filter(registered_at__isnull=False).count()
    summary['adherence'] = round(summary['saved_sets'] / summary['planned_sets'] * 100) if summary['planned_sets'] else 0
    completed = sessions.filter(status=WorkoutSession.Status.COMPLETED)
    weeks = list(completed.annotate(period=TruncWeek('date')).values('period').annotate(count=Count('pk')).order_by('-period')[:12])
    months = list(completed.annotate(period=TruncMonth('date')).values('period').annotate(count=Count('pk')).order_by('-period')[:12])
    volume = ExpressionWrapper(F('weight') * F('repetitions'), output_field=DecimalField(max_digits=14, decimal_places=2))
    saved = sets.filter(registered_at__isnull=False)
    if exercise:
        saved = saved.filter(session_exercise__exercise=exercise)
    performance = list(saved.values('session_exercise__exercise_id', 'session_exercise__exercise_name').annotate(series=Count('pk'), total_repetitions=Sum('repetitions'), max_weight=Max('weight'), volume=Sum(volume)).order_by('session_exercise__exercise_name'))
    evolution = []
    if exercise:
        evolution = list(saved.values('session_exercise__session_id', 'session_exercise__session__date', 'session_exercise__session__started_at').annotate(series=Count('pk'), total_repetitions=Sum('repetitions'), max_weight=Max('weight'), volume=Sum(volume)).order_by('-session_exercise__session__started_at')[:30])
        evolution.reverse()
    chart = {
        'labels': [f"{row['session_exercise__session__date']:%d/%m/%Y} · #{row['session_exercise__session_id']}" for row in evolution],
        'weights': [float(row['max_weight'] or Decimal(0)) for row in evolution],
        'repetitions': [row['total_repetitions'] for row in evolution],
    }
    return {'summary': summary, 'weeks': weeks, 'months': months, 'performance': performance, 'evolution': evolution, 'evolution_chart': chart}
