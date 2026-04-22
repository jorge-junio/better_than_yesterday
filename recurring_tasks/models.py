from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class RecurringTask(models.Model):
    class RecurrenceType(models.TextChoices):
        WEEKDAYS = 'weekdays', 'Dias da semana'
        DATE_RANGE = 'date_range', 'Intervalo de datas'
        SPECIFIC_DATES = 'specific_dates', 'Datas específicas'

    WEEKDAY_CHOICES = (
        ('mon', 'Segunda-feira'),
        ('tue', 'Terça-feira'),
        ('wed', 'Quarta-feira'),
        ('thu', 'Quinta-feira'),
        ('fri', 'Sexta-feira'),
        ('sat', 'Sábado'),
        ('sun', 'Domingo'),
    )

    name = models.CharField(max_length=500, verbose_name='nome')
    description = models.TextField(null=True, blank=True, verbose_name='descrição')
    estimated_time = models.DurationField(null=True, blank=True, verbose_name='tempo estimado')
    recurrence_type = models.CharField(
        max_length=20,
        choices=RecurrenceType.choices,
        verbose_name='tipo de recorrência',
    )
    weekdays = models.JSONField(default=list, blank=True, verbose_name='dias da semana')
    start_date = models.DateField(null=True, blank=True, verbose_name='data inicial')
    end_date = models.DateField(null=True, blank=True, verbose_name='data final')
    specific_dates = models.JSONField(default=list, blank=True, verbose_name='datas específicas')
    is_active = models.BooleanField(default=True, verbose_name='ativo')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Tarefa recorrente'
        verbose_name_plural = 'Tarefas recorrentes'
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=['name'],
                name='recurring_task_name_uk',
            )
        ]

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()

        if self.recurrence_type == self.RecurrenceType.WEEKDAYS:
            if not self.weekdays:
                raise ValidationError({'weekdays': 'Selecione pelo menos um dia da semana.'})
            invalid = [day for day in self.weekdays if day not in dict(self.WEEKDAY_CHOICES)]
            if invalid:
                raise ValidationError({'weekdays': f'Dias inválidos: {", ".join(invalid)}'})

        if self.recurrence_type == self.RecurrenceType.DATE_RANGE:
            if not self.start_date or not self.end_date:
                raise ValidationError('Informe a data inicial e a data final para recorrência por intervalo.')
            if self.start_date > self.end_date:
                raise ValidationError({'end_date': 'A data final deve ser maior ou igual à data inicial.'})

        if self.recurrence_type == self.RecurrenceType.SPECIFIC_DATES:
            if not self.specific_dates:
                raise ValidationError({'specific_dates': 'Informe ao menos uma data específica.'})

        if self.specific_dates:
            normalized_dates = []
            for raw_value in self.specific_dates:
                if isinstance(raw_value, str):
                    try:
                        parsed_date = timezone.datetime.strptime(raw_value, '%Y-%m-%d').date()
                    except ValueError as exc:
                        raise ValidationError({'specific_dates': f'Data inválida: {raw_value}'}) from exc
                    normalized_dates.append(parsed_date.isoformat())
                elif hasattr(raw_value, 'isoformat'):
                    normalized_dates.append(raw_value.isoformat())
                else:
                    raise ValidationError({'specific_dates': f'Data inválida: {raw_value}'})
            self.specific_dates = sorted(set(normalized_dates))

        if self.weekdays:
            self.weekdays = sorted(set(self.weekdays))

    @property
    def weekday_labels(self):
        labels = dict(self.WEEKDAY_CHOICES)
        return [labels[day] for day in self.weekdays if day in labels]

    @property
    def specific_dates_as_dates(self):
        dates = []
        for raw_value in self.specific_dates:
            if isinstance(raw_value, str):
                dates.append(timezone.datetime.strptime(raw_value, '%Y-%m-%d').date())
        return dates

    def occurs_on(self, date):
        if self.recurrence_type == self.RecurrenceType.WEEKDAYS:
            weekday_map = {
                0: 'mon',
                1: 'tue',
                2: 'wed',
                3: 'thu',
                4: 'fri',
                5: 'sat',
                6: 'sun',
            }
            return weekday_map[date.weekday()] in self.weekdays

        if self.recurrence_type == self.RecurrenceType.DATE_RANGE:
            if not self.start_date or not self.end_date:
                return False
            return self.start_date <= date <= self.end_date

        if self.recurrence_type == self.RecurrenceType.SPECIFIC_DATES:
            return date.isoformat() in self.specific_dates

        return False
