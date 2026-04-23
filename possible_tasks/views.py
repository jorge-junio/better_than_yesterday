from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from app.utils import HtmxTemplateMixin, PageTitleMixin, htmx_redirect, is_htmx_request

from . import forms, models


class PossibleTaskListView(HtmxTemplateMixin, PageTitleMixin, LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.PossibleTask
    template_name = 'possible_task_list.html'
    htmx_template_name = 'possible_tasks/partials/possible_task_list_content.html'
    page_title = 'BTY - Possíveis tarefas'
    context_object_name = 'possible_tasks'
    paginate_by = 20
    permission_required = 'possible_tasks.view_possibletask'

    def get_queryset(self):
        return super().get_queryset().order_by('-priority', 'title')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_task_base_url'] = reverse('task_create')
        context['create_recurring_task_base_url'] = reverse('recurring_task_create')
        return context


class PossibleTaskCreateView(HtmxTemplateMixin, PageTitleMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.PossibleTask
    template_name = 'possible_task_create.html'
    htmx_template_name = 'possible_tasks/partials/possible_task_form_content.html'
    page_title = 'BTY - Nova possível tarefa'
    form_class = forms.PossibleTaskForm
    success_url = reverse_lazy('possible_task_list')
    permission_required = 'possible_tasks.add_possibletask'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_heading'] = 'Cadastrar possível tarefa'
        context['submit_label'] = 'Salvar'
        context['cancel_url'] = reverse_lazy('possible_task_list')
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        if is_htmx_request(self.request):
            return htmx_redirect(self.get_success_url())
        return response


class PossibleTaskUpdateView(HtmxTemplateMixin, PageTitleMixin, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.PossibleTask
    template_name = 'possible_task_update.html'
    htmx_template_name = 'possible_tasks/partials/possible_task_form_content.html'
    page_title = 'BTY - Editar possível tarefa'
    form_class = forms.PossibleTaskForm
    success_url = reverse_lazy('possible_task_list')
    permission_required = 'possible_tasks.change_possibletask'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_heading'] = 'Editar possível tarefa'
        context['submit_label'] = 'Salvar'
        context['cancel_url'] = reverse_lazy('possible_task_list')
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        if is_htmx_request(self.request):
            return htmx_redirect(self.get_success_url())
        return response


class PossibleTaskDeleteView(HtmxTemplateMixin, PageTitleMixin, LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.PossibleTask
    template_name = 'possible_task_delete.html'
    htmx_template_name = 'possible_tasks/partials/possible_task_delete_content.html'
    page_title = 'BTY - Excluir possível tarefa'
    success_url = reverse_lazy('possible_task_list')
    permission_required = 'possible_tasks.delete_possibletask'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('possible_task_list')
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        if is_htmx_request(request):
            return htmx_redirect(success_url)
        return redirect(success_url)
