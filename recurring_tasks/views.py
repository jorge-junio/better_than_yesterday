from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from app.utils import HtmxTemplateMixin, PageTitleMixin, build_querystring, htmx_redirect, is_htmx_request

from . import forms, models


class RecurringTaskListView(HtmxTemplateMixin, PageTitleMixin, LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.RecurringTask
    queryset = models.RecurringTask.objects.select_related('category')
    template_name = 'recurring_task_list.html'
    htmx_template_name = 'recurring_tasks/partials/recurring_task_list_content.html'
    page_title = 'BTY - Tarefas recorrentes'
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query_string'] = build_querystring(self.request, exclude={'page'})
        return context


class RecurringTaskCreateView(HtmxTemplateMixin, PageTitleMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.RecurringTask
    template_name = 'recurring_task_create.html'
    htmx_template_name = 'recurring_tasks/partials/recurring_task_form_content.html'
    page_title = 'BTY - Tarefas recorrentes'
    form_class = forms.RecurringTaskForm
    success_url = reverse_lazy('recurring_task_list')
    permission_required = 'recurring_tasks.add_recurringtask'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_heading'] = 'Cadastrar Tarefa Recorrente'
        context['submit_label'] = 'Salvar tarefa recorrente'
        context['cancel_url'] = reverse_lazy('recurring_task_list')
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial['description'] = self.request.GET.get('description', '')
        return initial

    def form_valid(self, form):
        response = super().form_valid(form)
        if is_htmx_request(self.request):
            return htmx_redirect(self.get_success_url())
        return response


class RecurringTaskDetailView(HtmxTemplateMixin, PageTitleMixin, LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.RecurringTask
    queryset = models.RecurringTask.objects.select_related('category')
    template_name = 'recurring_task_detail.html'
    htmx_template_name = 'recurring_tasks/partials/recurring_task_detail_content.html'
    page_title = 'BTY - Tarefas recorrentes'
    permission_required = 'recurring_tasks.view_recurringtask'


class RecurringTaskUpdateView(HtmxTemplateMixin, PageTitleMixin, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.RecurringTask
    queryset = models.RecurringTask.objects.select_related('category')
    template_name = 'recurring_task_update.html'
    htmx_template_name = 'recurring_tasks/partials/recurring_task_form_content.html'
    page_title = 'BTY - Tarefas recorrentes'
    form_class = forms.RecurringTaskForm
    success_url = reverse_lazy('recurring_task_list')
    permission_required = 'recurring_tasks.change_recurringtask'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_heading'] = 'Editar Tarefa Recorrente'
        context['submit_label'] = 'Salvar tarefa recorrente'
        context['cancel_url'] = reverse_lazy('recurring_task_list')
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        if is_htmx_request(self.request):
            return htmx_redirect(self.get_success_url())
        return response


class RecurringTaskDeleteView(HtmxTemplateMixin, PageTitleMixin, LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.RecurringTask
    queryset = models.RecurringTask.objects.select_related('category')
    template_name = 'recurring_task_delete.html'
    htmx_template_name = 'recurring_tasks/partials/recurring_task_delete_content.html'
    page_title = 'BTY - Tarefas recorrentes'
    success_url = reverse_lazy('recurring_task_list')
    permission_required = 'recurring_tasks.delete_recurringtask'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('recurring_task_list')
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        if is_htmx_request(request):
            return htmx_redirect(success_url)
        return redirect(success_url)
