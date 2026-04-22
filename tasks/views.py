from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from . import forms, models, services


class TaskListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.Task
    template_name = 'task_list.html'
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
        show_completed = self.request.GET.get('show_completed')

        if show_completed not in {'1', 'true', 'True', 'on'}:
            queryset = queryset.filter(is_completed=False)

        return queryset.select_related('recurring_task')

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
            'show_completed': self.request.GET.get('show_completed') in {'1', 'true', 'True', 'on'},
        })
        return context


class TaskCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Task
    template_name = 'task_create.html'
    form_class = forms.TaskForm
    success_url = reverse_lazy('task_list')
    permission_required = 'tasks.add_task'

    def get_initial(self):
        initial = super().get_initial()
        initial['scheduled_date'] = timezone.localdate()
        return initial

    def form_valid(self, form):
        form.instance.source_type = models.Task.SourceType.MANUAL
        form.instance.recurring_task = None
        return super().form_valid(form)


class TaskDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Task
    template_name = 'task_detail.html'
    permission_required = 'tasks.view_task'


class TaskUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.Task
    template_name = 'task_update.html'
    form_class = forms.TaskForm
    success_url = reverse_lazy('task_list')
    permission_required = 'tasks.change_task'


class TaskDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Task
    template_name = 'task_delete.html'
    success_url = reverse_lazy('task_list')
    permission_required = 'tasks.delete_task'


class TaskToggleCompleteView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'tasks.change_task'

    def post(self, request, pk):
        task = get_object_or_404(models.Task, pk=pk)
        if task.is_completed:
            services.reopen_task(task)
        else:
            services.complete_task(task)
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
        return redirect(f"{reverse_lazy('task_list')}?scheduled_date={task.scheduled_date.isoformat()}")
