from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from app.utils import HtmxTemplateMixin, PageTitleMixin, htmx_redirect, is_htmx_request

from . import forms, models, services


class ProjectTaskListView(HtmxTemplateMixin, PageTitleMixin, LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.ProjectTask
    template_name = 'project_task_list.html'
    htmx_template_name = 'project_tasks/partials/project_task_list_content.html'
    page_title = 'BTY - Tarefas de projeto'
    context_object_name = 'project_tasks'
    paginate_by = 20
    permission_required = 'project_tasks.view_projecttask'

    def get_queryset(self):
        return super().get_queryset().select_related('project').order_by('-priority', 'title')


class ProjectTaskCreateView(HtmxTemplateMixin, PageTitleMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.ProjectTask
    template_name = 'project_task_create.html'
    htmx_template_name = 'project_tasks/partials/project_task_form_content.html'
    page_title = 'BTY - Tarefas de projeto'
    form_class = forms.ProjectTaskForm
    success_url = reverse_lazy('project_task_list')
    permission_required = 'project_tasks.add_projecttask'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_heading'] = 'Cadastrar Tarefa de Projeto'
        context['submit_label'] = 'Salvar tarefa'
        context['cancel_url'] = reverse_lazy('project_task_list')
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial['project'] = self.request.GET.get('project')
        return initial

    def form_valid(self, form):
        response = super().form_valid(form)
        if is_htmx_request(self.request):
            return htmx_redirect(self.get_success_url())
        return response


class ProjectTaskDetailView(HtmxTemplateMixin, PageTitleMixin, LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.ProjectTask
    template_name = 'project_task_detail.html'
    htmx_template_name = 'project_tasks/partials/project_task_detail_content.html'
    page_title = 'BTY - Tarefas de projeto'
    permission_required = 'project_tasks.view_projecttask'


class ProjectTaskUpdateView(HtmxTemplateMixin, PageTitleMixin, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.ProjectTask
    template_name = 'project_task_update.html'
    htmx_template_name = 'project_tasks/partials/project_task_form_content.html'
    page_title = 'BTY - Tarefas de projeto'
    form_class = forms.ProjectTaskForm
    success_url = reverse_lazy('project_task_list')
    permission_required = 'project_tasks.change_projecttask'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_heading'] = 'Editar Tarefa de Projeto'
        context['submit_label'] = 'Salvar tarefa'
        context['cancel_url'] = reverse_lazy('project_task_list')
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        if is_htmx_request(self.request):
            return htmx_redirect(self.get_success_url())
        return response


class ProjectTaskDeleteView(HtmxTemplateMixin, PageTitleMixin, LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.ProjectTask
    template_name = 'project_task_delete.html'
    htmx_template_name = 'project_tasks/partials/project_task_delete_content.html'
    page_title = 'BTY - Tarefas de projeto'
    success_url = reverse_lazy('project_task_list')
    permission_required = 'project_tasks.delete_projecttask'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('project_task_list')
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        if is_htmx_request(request):
            return htmx_redirect(success_url)
        return redirect(success_url)


class ProjectTaskToggleCompleteView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'project_tasks.change_projecttask'

    def post(self, request, pk):
        project_task = get_object_or_404(models.ProjectTask, pk=pk)
        if project_task.is_completed:
            services.reopen_project_task(project_task)
        else:
            services.complete_project_task(project_task)

        if is_htmx_request(request):
            return self.render_row(project_task)
        return redirect(reverse_lazy('project_task_list'))

    def render_row(self, project_task):
        from django.shortcuts import render

        return render(
            self.request,
            'project_tasks/partials/project_task_row.html',
            {'project_task': project_task},
        )
