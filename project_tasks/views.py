from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from app.utils import HtmxTemplateMixin, PageTitleMixin, build_querystring, htmx_redirect, is_htmx_request
from projects.models import Project
from projects import services as project_services

from possible_tasks import services as possible_task_services

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
        queryset = super().get_queryset().select_related('project').order_by('-priority', 'title')
        if 'project' in self.request.GET:
            project_id = self.request.GET.get('project')
        else:
            default_project = project_services.get_default_project()
            project_id = str(default_project.id) if default_project else None
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.order_by('title')
        if 'project' in self.request.GET:
            context['selected_project_id'] = self.request.GET.get('project') or ''
        else:
            default_project = project_services.get_default_project()
            context['selected_project_id'] = str(default_project.id) if default_project else ''
        context['query_string'] = build_querystring(self.request, exclude={'page'})
        return context


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
        context['possible_task_id'] = self.request.GET.get('possible_task')
        return context

    def get_initial(self):
        initial = super().get_initial()
        project_id = self.request.GET.get('project')
        possible_task_id = self.request.GET.get('possible_task')
        if possible_task_id:
            possible_task = possible_task_services.get_possible_task(possible_task_id)
            initial['title'] = possible_task.title
            initial['description'] = possible_task.description
            initial['priority'] = possible_task.priority
            if possible_task.project_id:
                project_id = possible_task.project_id
        if project_id:
            initial['project'] = project_id
        else:
            default_project = project_services.get_default_project()
            if default_project:
                initial['project'] = default_project.pk
        return initial

    def form_valid(self, form):
        possible_task_id = self.request.POST.get('possible_task_id')
        possible_task = possible_task_services.get_possible_task(possible_task_id) if possible_task_id else None
        response = super().form_valid(form)
        if possible_task:
            possible_task_services.link_possible_task_to_generated_object(possible_task, self.object)
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
        possible_task_id = self.request.POST.get('possible_task_id')
        possible_task = possible_task_services.get_possible_task(possible_task_id) if possible_task_id else None
        response = super().form_valid(form)
        if possible_task:
            possible_task_services.link_possible_task_to_generated_object(possible_task, self.object)
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
