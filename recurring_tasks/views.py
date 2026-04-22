from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from . import forms, models


class RecurringTaskListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.RecurringTask
    template_name = 'recurring_task_list.html'
    context_object_name = 'recurring_tasks'
    paginate_by = 10
    permission_required = 'recurring_tasks.view_recurringtask'

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')
        recurrence_type = self.request.GET.get('recurrence_type')
        is_active = self.request.GET.get('is_active')

        if name:
            queryset = queryset.filter(name__icontains=name)

        if recurrence_type:
            queryset = queryset.filter(recurrence_type=recurrence_type)

        if is_active in {'0', '1'}:
            queryset = queryset.filter(is_active=bool(int(is_active)))

        return queryset


class RecurringTaskCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.RecurringTask
    template_name = 'recurring_task_create.html'
    form_class = forms.RecurringTaskForm
    success_url = reverse_lazy('recurring_task_list')
    permission_required = 'recurring_tasks.add_recurringtask'


class RecurringTaskDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.RecurringTask
    template_name = 'recurring_task_detail.html'
    permission_required = 'recurring_tasks.view_recurringtask'


class RecurringTaskUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.RecurringTask
    template_name = 'recurring_task_update.html'
    form_class = forms.RecurringTaskForm
    success_url = reverse_lazy('recurring_task_list')
    permission_required = 'recurring_tasks.change_recurringtask'


class RecurringTaskDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.RecurringTask
    template_name = 'recurring_task_delete.html'
    success_url = reverse_lazy('recurring_task_list')
    permission_required = 'recurring_tasks.delete_recurringtask'
