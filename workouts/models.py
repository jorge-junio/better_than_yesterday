import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.functions import Lower

WEEKDAYS = [
    (0, 'Segunda-feira'), (1, 'Terça-feira'), (2, 'Quarta-feira'),
    (3, 'Quinta-feira'), (4, 'Sexta-feira'), (5, 'Sábado'), (6, 'Domingo'),
]


class Exercise(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    name = models.CharField('nome', max_length=160)

    class Meta:
        ordering = ['name']
        verbose_name = 'Exercício'
        verbose_name_plural = 'Exercícios'
        constraints = [models.UniqueConstraint(Lower('name'), 'owner', name='workouts_unique_exercise_name')]

    def __str__(self):
        return self.name


class Workout(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    name = models.CharField('nome', max_length=160)
    start_date = models.DateField('data de início')
    end_date = models.DateField('data final', null=True, blank=True)
    rest_seconds = models.PositiveIntegerField('descanso entre séries (segundos)', default=60, validators=[MaxValueValidator(3600)])
    is_active = models.BooleanField('ativo', default=False)
    is_archived = models.BooleanField('arquivado', default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_active', '-created_at']
        verbose_name = 'Treino'
        verbose_name_plural = 'Treinos'
        constraints = [
            models.UniqueConstraint(fields=['owner'], condition=models.Q(is_active=True), name='workouts_one_active_per_owner'),
            models.CheckConstraint(condition=models.Q(end_date__isnull=True) | models.Q(end_date__gte=models.F('start_date')), name='workouts_valid_date_range'),
            models.CheckConstraint(condition=~models.Q(is_archived=True, is_active=True), name='workouts_archived_not_active'),
            models.CheckConstraint(condition=models.Q(rest_seconds__lte=3600), name='workouts_valid_rest_seconds'),
        ]

    def clean(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValidationError({'end_date': 'A data final deve ser igual ou posterior à data de início.'})
        if self.is_archived and self.is_active:
            raise ValidationError('Um treino arquivado não pode estar ativo.')

    def is_valid_on(self, date):
        return self.start_date <= date and (self.end_date is None or date <= self.end_date)

    def __str__(self):
        return self.name


class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.PROTECT)
    weekday = models.PositiveSmallIntegerField('dia da semana', choices=WEEKDAYS)
    position = models.PositiveSmallIntegerField('ordem', default=1, validators=[MinValueValidator(1)])
    sets_count = models.PositiveSmallIntegerField('séries', validators=[MinValueValidator(1), MaxValueValidator(100)])
    repetitions = models.PositiveSmallIntegerField('repetições por série', validators=[MinValueValidator(1), MaxValueValidator(1000)])
    notes = models.TextField('observações', blank=True)

    class Meta:
        ordering = ['weekday', 'position', 'pk']
        verbose_name = 'Exercício do treino'
        verbose_name_plural = 'Exercícios do treino'
        constraints = [
            models.CheckConstraint(condition=models.Q(weekday__lte=6), name='workouts_valid_weekday'),
            models.CheckConstraint(condition=models.Q(sets_count__gte=1, repetitions__gte=1, position__gte=1), name='workouts_positive_plan'),
        ]

    def clean(self):
        if self.workout_id and self.exercise_id and self.workout.owner_id != self.exercise.owner_id:
            raise ValidationError('O exercício deve pertencer ao usuário do treino.')

    def __str__(self):
        return f'{self.exercise} — {self.get_weekday_display()}'


class WorkoutSession(models.Model):
    class Status(models.TextChoices):
        IN_PROGRESS = 'in_progress', 'Em andamento'
        COMPLETED = 'completed', 'Concluída'
        PARTIAL = 'partial', 'Parcial'

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    workout = models.ForeignKey(Workout, on_delete=models.PROTECT, related_name='sessions')
    workout_name = models.CharField(max_length=160)
    rest_seconds = models.PositiveIntegerField(default=60, validators=[MaxValueValidator(3600)])
    scheduled_weekday = models.PositiveSmallIntegerField(choices=WEEKDAYS)
    date = models.DateField('data')
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField('situação', max_length=20, choices=Status.choices, default=Status.IN_PROGRESS)
    request_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    class Meta:
        ordering = ['-started_at', '-pk']
        verbose_name = 'Sessão de treino'
        verbose_name_plural = 'Sessões de treino'
        constraints = [
            models.UniqueConstraint(fields=['owner'], condition=models.Q(status='in_progress'), name='workouts_one_open_session'),
            models.CheckConstraint(condition=models.Q(scheduled_weekday__lte=6), name='workouts_valid_session_weekday'),
            models.CheckConstraint(condition=models.Q(rest_seconds__lte=3600), name='workouts_valid_session_rest'),
        ]
        indexes = [models.Index(fields=['owner', 'date'])]

    @property
    def is_open(self):
        return self.status == self.Status.IN_PROGRESS

    @property
    def duration_minutes(self):
        if self.finished_at:
            return int((self.finished_at - self.started_at).total_seconds() // 60)
        return None

    def __str__(self):
        return f'{self.workout_name} — {self.date:%d/%m/%Y}'


class SessionExercise(models.Model):
    session = models.ForeignKey(WorkoutSession, on_delete=models.CASCADE, related_name='exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.PROTECT)
    exercise_name = models.CharField(max_length=160)
    position = models.PositiveSmallIntegerField()
    target_sets = models.PositiveSmallIntegerField()
    target_repetitions = models.PositiveSmallIntegerField()
    notes = models.TextField(blank=True)
    is_skipped = models.BooleanField(default=False)

    class Meta:
        ordering = ['position', 'pk']
        verbose_name = 'Exercício da sessão'
        verbose_name_plural = 'Exercícios da sessão'


class SessionSet(models.Model):
    session_exercise = models.ForeignKey(SessionExercise, on_delete=models.CASCADE, related_name='sets')
    number = models.PositiveSmallIntegerField('série')
    repetitions = models.PositiveSmallIntegerField('repetições realizadas', null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(1000)])
    weight = models.DecimalField('peso (kg)', max_digits=7, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    registered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['number']
        verbose_name = 'Série realizada'
        verbose_name_plural = 'Séries realizadas'
        constraints = [
            models.UniqueConstraint(fields=['session_exercise', 'number'], name='workouts_unique_set_number'),
            models.CheckConstraint(condition=models.Q(number__gte=1), name='workouts_positive_set_number'),
            models.CheckConstraint(condition=models.Q(weight__gte=0) | models.Q(weight__isnull=True), name='workouts_nonnegative_weight'),
            models.CheckConstraint(condition=(models.Q(registered_at__isnull=True, repetitions__isnull=True, weight__isnull=True) | models.Q(registered_at__isnull=False, repetitions__isnull=False, weight__isnull=False)), name='workouts_complete_set_record'),
        ]
