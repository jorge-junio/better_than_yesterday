from datetime import datetime, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from app.utils import HtmxTemplateMixin, PageTitleMixin, build_querystring, htmx_redirect, is_htmx_request

from . import forms, models, services


def parse_time_spent_parts(post_data):
    values = {}
    for key in ('hours', 'minutes', 'seconds'):
        raw_value = (post_data.get(f'time_spent_{key}') or '0').strip()
        try:
            parsed_value = int(raw_value)
        except ValueError:
            return None, 'Use apenas números inteiros nos campos de tempo.'

        if parsed_value < 0:
            return None, 'Os campos de tempo não podem ser negativos.'

        values[key] = parsed_value

    return timedelta(
        hours=values['hours'],
        minutes=values['minutes'],
        seconds=values['seconds'],
    ), None


class TaskListView(HtmxTemplateMixin, PageTitleMixin, LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.Task
    template_name = 'task_list.html'
    htmx_template_name = 'tasks/partials/task_list_content.html'
    page_title = 'BTY - Agenda do Dia'
    context_object_name = 'tasks'
    paginate_by = 20
    permission_required = 'tasks.view_task'

    def get_selected_date(self):
        raw_date = self.request.GET.get('scheduled_date')
        if not raw_date:
            return timezone.localdate()
        try:
            return datetime.strptime(raw_date, '%Y-%m-%d').date()
        except ValueError:
            raise Http404('Data inválida.')

    def get_queryset(self):
        selected_date = self.get_selected_date()
        services.ensure_tasks_for_date(selected_date)

        queryset = super().get_queryset().filter(scheduled_date=selected_date)
        status = self.request.GET.get('status') or forms.TaskFilterForm.StatusChoices.ALL
        category_id = self.request.GET.get('category')

        if status == forms.TaskFilterForm.StatusChoices.COMPLETED:
            queryset = queryset.filter(is_completed=True)
        elif status == forms.TaskFilterForm.StatusChoices.PENDING:
            queryset = queryset.filter(is_completed=False, skipped_in__isnull=True)
        elif status == forms.TaskFilterForm.StatusChoices.POSTPONED:
            queryset = queryset.filter(skipped_in__isnull=False)
        else:
            status = forms.TaskFilterForm.StatusChoices.ALL

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset.select_related('recurring_task', 'category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_date = self.get_selected_date()
        total = models.Task.objects.filter(scheduled_date=selected_date).count()
        completed = models.Task.objects.filter(
            scheduled_date=selected_date,
            is_completed=True,
        ).count()

        context['selected_date'] = selected_date
        context['total_tasks'] = total
        context['completed_tasks'] = completed
        context['completion_rate'] = int((completed / total) * 100) if total else 0
        context['filter_form'] = forms.TaskFilterForm(self.request.GET or None, initial={
            'scheduled_date': selected_date,
            'status': self.request.GET.get('status') or forms.TaskFilterForm.StatusChoices.ALL,
            'category': self.request.GET.get('category') or '',
        })
        context['query_string'] = build_querystring(self.request, exclude={'page'})
        return context


class TaskTodayView(HtmxTemplateMixin, PageTitleMixin, LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'task_today.html'
    htmx_template_name = 'tasks/partials/today_mission_content.html'
    page_title = 'BTY - Missão do Dia'
    permission_required = 'tasks.view_task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(services.get_today_mission_context())
        return context


class TaskCreateView(HtmxTemplateMixin, PageTitleMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Task
    template_name = 'task_create.html'
    htmx_template_name = 'tasks/partials/task_form_content.html'
    page_title = 'BTY - Nova Tarefa'
    form_class = forms.TaskForm
    success_url = reverse_lazy('task_list')
    permission_required = 'tasks.add_task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_heading'] = 'Cadastrar Tarefa'
        context['submit_label'] = 'Salvar'
        context['cancel_url'] = reverse_lazy('task_list')
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial['scheduled_date'] = timezone.localdate()
        initial['description'] = self.request.GET.get('description', '')
        return initial

    def form_valid(self, form):
        form.instance.source_type = models.Task.SourceType.MANUAL
        form.instance.recurring_task = None
        response = super().form_valid(form)
        if is_htmx_request(self.request):
            return htmx_redirect(self.get_success_url())
        return response


class TaskDetailView(HtmxTemplateMixin, PageTitleMixin, LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Task
    queryset = models.Task.objects.select_related('recurring_task', 'category')
    template_name = 'task_detail.html'
    htmx_template_name = 'tasks/partials/task_detail_content.html'
    page_title = 'BTY - Detalhe da Tarefa'
    permission_required = 'tasks.view_task'


class TaskUpdateView(HtmxTemplateMixin, PageTitleMixin, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.Task
    queryset = models.Task.objects.select_related('recurring_task', 'category')
    template_name = 'task_update.html'
    htmx_template_name = 'tasks/partials/task_form_content.html'
    page_title = 'BTY - Editar Tarefa'
    form_class = forms.TaskForm
    success_url = reverse_lazy('task_list')
    permission_required = 'tasks.change_task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_heading'] = 'Editar Tarefa'
        context['submit_label'] = 'Salvar'
        context['cancel_url'] = reverse_lazy('task_list')
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        if is_htmx_request(self.request):
            return htmx_redirect(self.get_success_url())
        return response


class TaskDeleteView(HtmxTemplateMixin, PageTitleMixin, LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Task
    queryset = models.Task.objects.select_related('recurring_task', 'category')
    template_name = 'task_delete.html'
    htmx_template_name = 'tasks/partials/task_delete_content.html'
    page_title = 'BTY - Excluir Tarefa'
    success_url = reverse_lazy('task_list')
    permission_required = 'tasks.delete_task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('task_list')
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        if is_htmx_request(request):
            return htmx_redirect(success_url)
        return redirect(success_url)


class TaskToggleCompleteView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'tasks.change_task'

    def post(self, request, pk):
        task = get_object_or_404(models.Task, pk=pk)
        if task.is_completed:
            services.reopen_task(task)
        else:
            services.complete_task(task)
        if is_htmx_request(request):
            return render(request, 'tasks/partials/task_row.html', {'task': task})
        return redirect(self.get_success_url(task))

    def get_success_url(self, task):
        return f"{reverse_lazy('task_list')}?scheduled_date={task.scheduled_date.isoformat()}"


class TaskPostponeView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'tasks.change_task'

    def post(self, request, pk):
        task = get_object_or_404(models.Task, pk=pk)
        days = request.POST.get('days', '1')
        try:
            days_int = int(days)
        except ValueError as exc:
            raise Http404('Número de dias inválido.') from exc

        services.postpone_task(task, days=days_int)
        if is_htmx_request(request):
            return render(request, 'tasks/partials/task_row.html', {'task': task})
        return redirect(f"{reverse_lazy('task_list')}?scheduled_date={task.scheduled_date.isoformat()}")


class TaskTodayCompleteView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'tasks.change_task'

    def post(self, request, pk):
        reference_date = timezone.localdate()
        task = get_object_or_404(models.Task, pk=pk, scheduled_date=reference_date)
        parsed_time_spent, error_message = parse_time_spent_parts(request.POST)
        if error_message:
            context = services.get_today_mission_context(reference_date=reference_date)
            context['page_title'] = 'BTY - Missão do Dia'
            context['message_error'] = error_message
            if is_htmx_request(request):
                return render(request, 'tasks/partials/today_mission_content.html', context)
            return redirect(reverse_lazy('task_today'))

        services.complete_task(
            task,
            time_spent=parsed_time_spent,
        )

        if is_htmx_request(request):
            context = services.get_today_mission_context(reference_date=reference_date)
            context['page_title'] = 'BTY - Missão do Dia'
            return render(request, 'tasks/partials/today_mission_content.html', context)

        return redirect(reverse_lazy('task_today'))


class TaskTodayStartView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'tasks.change_task'

    def post(self, request, pk):
        reference_date = timezone.localdate()
        task = get_object_or_404(models.Task, pk=pk, scheduled_date=reference_date)
        services.start_task(task)

        if is_htmx_request(request):
            context = services.get_today_mission_context(reference_date=reference_date)
            context['page_title'] = 'BTY - Missão do Dia'
            return render(request, 'tasks/partials/today_mission_content.html', context)

        return redirect(reverse_lazy('task_today'))


class TaskTodaySkipView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'tasks.change_task'

    def post(self, request, pk):
        reference_date = timezone.localdate()
        task = get_object_or_404(models.Task, pk=pk, scheduled_date=reference_date)
        services.skip_task_for_today(task)

        if is_htmx_request(request):
            context = services.get_today_mission_context(reference_date=reference_date)
            context['page_title'] = 'BTY - Missão do Dia'
            return render(request, 'tasks/partials/today_mission_content.html', context)

        return redirect(reverse_lazy('task_today'))
