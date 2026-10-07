import json

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied, ValidationError
from django.http import Http404, HttpResponseBadRequest
from django.core.paginator import Paginator
from django.db.models import Max
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views import View

from app.utils import is_htmx_request, htmx_redirect, build_querystring
from . import forms, models, services


def navigate(request, name, **kwargs):
    url = reverse(name, kwargs=kwargs)
    return htmx_redirect(url) if is_htmx_request(request) else redirect(url)


class WorkoutView(LoginRequiredMixin, PermissionRequiredMixin, View):
    page_title = 'BTY - Treinos'
    workout_section = 'workout'

    def display(self, request, partial, context=None):
        context = {'page_title': self.page_title, 'workout_section': self.workout_section, 'content_template': f'workouts/partials/{partial}.html', **(context or {})}
        template = context['content_template'] if is_htmx_request(request) else 'workouts/page.html'
        return render(request, template, context)


class WorkoutListView(WorkoutView):
    permission_required = 'workouts.view_workout'

    def get(self, request):
        queryset = models.Workout.objects.filter(owner=request.user)
        archived = request.GET.get('archived') == '1'
        queryset = queryset.filter(is_archived=archived)
        page = Paginator(queryset, 20).get_page(request.GET.get('page'))
        return self.display(request, 'workout_list', {'workouts': page, 'page_obj': page, 'archived': archived, 'query_string': build_querystring(request, exclude={'page'})})


class WorkoutFormView(WorkoutView):
    def get_permission_required(self):
        return ('workouts.change_workout' if self.kwargs.get('pk') else 'workouts.add_workout',)

    def get_workout(self, request, pk):
        if pk:
            return get_object_or_404(models.Workout, pk=pk, owner=request.user, is_archived=False)
        return models.Workout(owner=request.user)

    def display_form(self, request, form):
        return self.display(request, 'form', {'form': form, 'heading': 'Editar treino' if form.instance.pk else 'Novo treino', 'cancel_url': reverse('workout_detail', args=[form.instance.pk]) if form.instance.pk else reverse('workout_list'), 'submit_label': 'Salvar treino'})

    def get(self, request, pk=None):
        return self.display_form(request, forms.WorkoutForm(instance=self.get_workout(request, pk), owner=request.user))

    def post(self, request, pk=None):
        form = forms.WorkoutForm(request.POST, instance=self.get_workout(request, pk), owner=request.user)
        if form.is_valid():
            try:
                workout = services.save_workout(form, request.user)
                return navigate(request, 'workout_detail', pk=workout.pk)
            except ValidationError as exc:
                form = forms.WorkoutForm(request.POST, instance=self.get_workout(request, pk), owner=request.user)
                form.is_valid()
                form.add_error(None, exc)
        return self.display_form(request, form)


class WorkoutDetailView(WorkoutView):
    permission_required = 'workouts.view_workout'

    def get(self, request, pk):
        workout = get_object_or_404(models.Workout, pk=pk, owner=request.user)
        return self.display(request, 'workout_detail', {'workout': workout, 'days': services.weekly_program(workout)})


class WorkoutArchiveView(WorkoutView):
    permission_required = 'workouts.change_workout'

    def get(self, request, pk):
        workout = get_object_or_404(models.Workout, pk=pk, owner=request.user)
        return self.display(request, 'confirmation', {'heading': 'Restaurar treino' if workout.is_archived else 'Arquivar treino', 'description': 'O histórico será preservado. Ao restaurar, o treino permanece inativo.', 'cancel_url': reverse('workout_detail', args=[pk]), 'submit_label': 'Restaurar' if workout.is_archived else 'Arquivar', 'archive_action': 'restore' if workout.is_archived else 'archive'})

    def post(self, request, pk):
        get_object_or_404(models.Workout, pk=pk, owner=request.user)
        action = request.POST.get('archive_action')
        if action not in ['archive', 'restore']:
            return HttpResponseBadRequest('Ação de arquivamento inválida.')
        services.set_archived(pk, request.user, action == 'archive')
        return navigate(request, 'workout_list')


class WorkoutExerciseFormView(WorkoutView):
    def get_permission_required(self):
        return ('workouts.change_workoutexercise' if self.kwargs.get('entry_id') else 'workouts.add_workoutexercise',)

    def get_entry(self, request, workout_id, entry_id):
        workout = get_object_or_404(models.Workout, pk=workout_id, owner=request.user, is_archived=False)
        return get_object_or_404(models.WorkoutExercise, pk=entry_id, workout=workout) if entry_id else models.WorkoutExercise(workout=workout)

    def display_form(self, request, form, workout_id):
        return self.display(request, 'form', {'form': form, 'heading': 'Editar exercício' if form.instance.pk else 'Adicionar exercício', 'submit_label': 'Salvar exercício', 'cancel_url': reverse('workout_detail', args=[workout_id])})

    def get(self, request, workout_id, entry_id=None):
        entry = self.get_entry(request, workout_id, entry_id)
        weekday = request.GET.get('weekday', timezone.localdate().weekday())
        last = entry.workout.exercises.filter(weekday=weekday).aggregate(last=Max('position'))['last'] if str(weekday) in [str(day) for day, _ in models.WEEKDAYS] else None
        form = forms.WorkoutExerciseForm(instance=entry, owner=request.user, initial={'weekday': weekday, 'position': (last or 0) + 1, 'sets_count': 3, 'repetitions': 12} if not entry.pk else None)
        return self.display_form(request, form, workout_id)

    def post(self, request, workout_id, entry_id=None):
        form = forms.WorkoutExerciseForm(request.POST, instance=self.get_entry(request, workout_id, entry_id), owner=request.user)
        if form.is_valid():
            try:
                services.save_workout_exercise(form, workout_id, request.user)
                return navigate(request, 'workout_detail', pk=workout_id)
            except ValidationError as exc:
                form.add_error(None, exc)
        return self.display_form(request, form, workout_id)


class WorkoutDayCopyView(WorkoutView):
    permission_required = ('workouts.view_workout', 'workouts.add_workoutexercise')

    def get_workout(self, request, workout_id, source_weekday):
        if source_weekday not in dict(models.WEEKDAYS):
            raise Http404
        return get_object_or_404(models.Workout, pk=workout_id, owner=request.user, is_archived=False)

    def display_form(self, request, workout, source_weekday, form):
        source_label = dict(models.WEEKDAYS)[source_weekday]
        count = workout.exercises.filter(weekday=source_weekday).count()
        return self.display(request, 'form', {
            'form': form, 'heading': f'Copiar programação de {source_label}',
            'description': f'{count} exercício(s) de “{workout.name}” serão copiados com as séries, repetições e observações. A programação de origem e o histórico serão preservados.',
            'submit_label': 'Copiar exercícios', 'cancel_url': reverse('workout_detail', args=[workout.pk]),
        })

    def get(self, request, workout_id, source_weekday):
        workout = self.get_workout(request, workout_id, source_weekday)
        form = forms.CopyWorkoutDayForm(source_weekday=source_weekday)
        return self.display_form(request, workout, source_weekday, form)

    def post(self, request, workout_id, source_weekday):
        workout = self.get_workout(request, workout_id, source_weekday)
        form = forms.CopyWorkoutDayForm(request.POST, source_weekday=source_weekday)
        if form.is_valid():
            try:
                services.copy_workout_day(workout_id, request.user, source_weekday, form.cleaned_data['destination_weekday'])
                return navigate(request, 'workout_detail', pk=workout_id)
            except ValidationError as exc:
                form.add_error(None, exc)
        return self.display_form(request, workout, source_weekday, form)


class WorkoutExerciseRemoveView(WorkoutView):
    permission_required = 'workouts.delete_workoutexercise'

    def get_entry(self, request, entry_id):
        return get_object_or_404(models.WorkoutExercise.objects.select_related('exercise'), pk=entry_id, workout__owner=request.user, workout__is_archived=False)

    def get(self, request, entry_id):
        entry = self.get_entry(request, entry_id)
        return self.display(request, 'confirmation', {'heading': f'Remover {entry.exercise.name}', 'description': 'O exercício será removido da programação. As sessões já iniciadas e o histórico permanecem intactos.', 'cancel_url': reverse('workout_detail', args=[entry.workout_id]), 'submit_label': 'Remover exercício'})

    def post(self, request, entry_id):
        entry = self.get_entry(request, entry_id)
        try:
            services.remove_workout_exercise(entry_id, request.user)
        except ValidationError as exc:
            return self.display(request, 'confirmation', {'heading': 'Não foi possível remover', 'error': exc.messages, 'cancel_url': reverse('workout_detail', args=[entry.workout_id]), 'submit_label': 'Tentar novamente'})
        return navigate(request, 'workout_detail', pk=entry.workout_id)


class TrainView(WorkoutView):
    permission_required = 'workouts.view_workoutsession'
    page_title = 'BTY - Treinar'
    workout_section = 'train'

    def display_start(self, request, form):
        active = models.Workout.objects.filter(owner=request.user, is_active=True, is_archived=False).first()
        ongoing = models.WorkoutSession.objects.filter(owner=request.user, status='in_progress').first()
        valid = active and active.is_valid_on(timezone.localdate())
        return self.display(request, 'train', {'form': form, 'active': active, 'ongoing': ongoing, 'valid': valid, 'days': services.weekly_program(active) if active else [], 'today': timezone.localdate()})

    def get(self, request):
        return self.display_start(request, forms.StartSessionForm())

    def post(self, request):
        if not request.user.has_perm('workouts.add_workoutsession'):
            raise PermissionDenied
        form = forms.StartSessionForm(request.POST)
        if form.is_valid():
            try:
                session = services.start_session(request.user, **form.cleaned_data)
                return navigate(request, 'workout_session', pk=session.pk)
            except ValidationError as exc:
                form.add_error(None, exc)
        return self.display_start(request, form)


class SessionView(WorkoutView):
    permission_required = 'workouts.view_workoutsession'
    page_title = 'BTY - Sessão de treino'

    def get(self, request, pk):
        session = get_object_or_404(models.WorkoutSession, pk=pk, owner=request.user)
        cards = services.session_cards(session)
        editable = session.is_open and request.user.has_perm('workouts.change_workoutsession')
        for card in cards:
            card['rows'] = [{'series': series, 'form': forms.SessionSetForm(instance=series, prefix=f'set-{series.pk}')} for series in card['item'].sets.all()]
        return self.display(request, 'session', {'session': session, 'cards': cards, 'editable': editable, 'workout_section': 'train' if session.is_open else 'history', 'progress': services.session_progress(session)})


class SessionSetView(WorkoutView):
    workout_section = 'train'
    permission_required = 'workouts.change_workoutsession'
    http_method_names = ['post']

    def post(self, request, set_id):
        series = get_object_or_404(models.SessionSet.objects.select_related('session_exercise__session'), pk=set_id, session_exercise__session__owner=request.user)
        session = series.session_exercise.session
        form = forms.SessionSetForm(request.POST, instance=series, prefix=f'set-{series.pk}')
        saved = False
        if form.is_valid():
            try:
                series = services.record_set(set_id, request.user, **form.cleaned_data)
                form = forms.SessionSetForm(instance=series, prefix=f'set-{series.pk}')
                saved = True
            except ValidationError as exc:
                form.add_error(None, exc)
        if not is_htmx_request(request):
            if saved:
                return navigate(request, 'workout_session', pk=session.pk)
            return self.display(request, 'form', {'form': form, 'heading': 'Corrigir série', 'submit_label': 'Registrar série', 'cancel_url': reverse('workout_session', args=[session.pk])})
        response = render(request, 'workouts/partials/set_response.html', {'series': series, 'form': form, 'session': session, 'item': series.session_exercise, 'saved': saved, 'progress': services.session_progress(session)})
        if saved and series.was_new_registration and session.rest_seconds:
            response['HX-Trigger-After-Swap'] = json.dumps({
                'workoutRestStarted': {'sessionId': session.pk, 'setId': series.pk, 'seconds': session.rest_seconds},
            })
        return response


class SessionSkipView(WorkoutView):
    workout_section = 'train'
    permission_required = 'workouts.change_workoutsession'
    http_method_names = ['post']

    def post(self, request, exercise_id):
        item = get_object_or_404(models.SessionExercise, pk=exercise_id, session__owner=request.user)
        action = request.POST.get('exercise_action')
        if action not in ['skip', 'resume']:
            return HttpResponseBadRequest('Ação do exercício inválida.')
        try:
            services.set_skipped(exercise_id, request.user, action == 'skip')
        except ValidationError as exc:
            return self.display(request, 'notice', {'error': exc.messages, 'cancel_url': reverse('workout_session', args=[item.session_id])})
        return navigate(request, 'workout_session', pk=item.session_id)


class SessionFinishView(WorkoutView):
    workout_section = 'train'
    permission_required = 'workouts.change_workoutsession'

    def context(self, request, pk):
        session = get_object_or_404(models.WorkoutSession, pk=pk, owner=request.user)
        return {'session': session, 'progress': services.session_progress(session), 'cancel_url': reverse('workout_session', args=[pk])}

    def get(self, request, pk):
        context = self.context(request, pk)
        if not context['session'].is_open:
            return navigate(request, 'workout_session', pk=pk)
        return self.display(request, 'finish', context)

    def post(self, request, pk):
        context = self.context(request, pk)
        try:
            services.finish_session(pk, request.user, request.POST.get('confirm_partial') == 'on')
            return navigate(request, 'workout_session', pk=pk)
        except ValidationError as exc:
            context['error'] = exc.messages
            return self.display(request, 'finish', context)


class HistoryView(WorkoutView):
    permission_required = 'workouts.view_workoutsession'
    page_title = 'BTY - Histórico de treinos'
    workout_section = 'history'

    def get(self, request):
        form = forms.HistoryFilterForm(request.GET or None, owner=request.user)
        data = form.cleaned_data if form.is_bound and form.is_valid() else {}
        queryset = services.filter_sessions(request.user, data)
        if form.is_bound and not form.is_valid():
            queryset = queryset.none()
        page = Paginator(services.annotate_sessions(queryset), 20).get_page(request.GET.get('page'))
        reports = services.build_reports(queryset, data.get('exercise'))
        return self.display(request, 'history', {'form': form, 'sessions': page, 'page_obj': page, 'query_string': build_querystring(request, exclude={'page'}), 'selected_exercise': data.get('exercise'), **reports})
