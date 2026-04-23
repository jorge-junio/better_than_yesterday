from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from app.utils import HtmxTemplateMixin, PageTitleMixin, htmx_redirect, is_htmx_request

from . import forms, models


class ProjectListView(HtmxTemplateMixin, PageTitleMixin, LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.Project
    template_name = 'project_list.html'
    htmx_template_name = 'projects/partials/project_list_content.html'
    page_title = 'BTY - Projetos'
    context_object_name = 'projects'
    paginate_by = 20
    permission_required = 'projects.view_project'


class ProjectCreateView(HtmxTemplateMixin, PageTitleMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Project
    template_name = 'project_create.html'
    htmx_template_name = 'projects/partials/project_form_content.html'
    page_title = 'BTY - Projetos'
    form_class = forms.ProjectForm
    success_url = reverse_lazy('project_list')
    permission_required = 'projects.add_project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_heading'] = 'Cadastrar Projeto'
        context['submit_label'] = 'Salvar projeto'
        context['cancel_url'] = reverse_lazy('project_list')
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        if is_htmx_request(self.request):
            return htmx_redirect(self.get_success_url())
        return response


class ProjectDetailView(HtmxTemplateMixin, PageTitleMixin, LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Project
    template_name = 'project_detail.html'
    htmx_template_name = 'projects/partials/project_detail_content.html'
    page_title = 'BTY - Projetos'
    permission_required = 'projects.view_project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_tasks_count'] = self.object.project_tasks.count()
        return context


class ProjectUpdateView(HtmxTemplateMixin, PageTitleMixin, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.Project
    template_name = 'project_update.html'
    htmx_template_name = 'projects/partials/project_form_content.html'
    page_title = 'BTY - Projetos'
    form_class = forms.ProjectForm
    success_url = reverse_lazy('project_list')
    permission_required = 'projects.change_project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_heading'] = 'Editar Projeto'
        context['submit_label'] = 'Salvar projeto'
        context['cancel_url'] = reverse_lazy('project_list')
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        if is_htmx_request(self.request):
            return htmx_redirect(self.get_success_url())
        return response


class ProjectDeleteView(HtmxTemplateMixin, PageTitleMixin, LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Project
    template_name = 'project_delete.html'
    htmx_template_name = 'projects/partials/project_delete_content.html'
    page_title = 'BTY - Projetos'
    success_url = reverse_lazy('project_list')
    permission_required = 'projects.delete_project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('project_list')
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        if is_htmx_request(request):
            return htmx_redirect(success_url)
        return redirect(success_url)
