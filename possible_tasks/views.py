from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from app.utils import HtmxTemplateMixin, PageTitleMixin, build_querystring, htmx_redirect, is_htmx_request
from projects import services as project_services
from projects.models import Project

from . import forms, models
from . import services as possible_task_services


class PossibleTaskListView(HtmxTemplateMixin, PageTitleMixin, LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.PossibleTask
    template_name = 'possible_task_list.html'
    htmx_template_name = 'possible_tasks/partials/possible_task_list_content.html'
    page_title = 'BTY - Possíveis tarefas'
    context_object_name = 'possible_tasks'
    paginate_by = 20
    permission_required = 'possible_tasks.view_possibletask'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('project').order_by('-priority', 'title')
        project_id = self.request.GET.get('project')
        conversion = self.request.GET.get('conversion') or 'not_converted'
        if project_id == 'none':
            queryset = queryset.filter(project__isnull=True)
        elif project_id:
            queryset = queryset.filter(project_id=project_id)

        if conversion == 'converted':
            queryset = queryset.filter(
                Q(generated_task__isnull=False)
                | Q(generated_recurring_task__isnull=False)
                | Q(generated_project_task__isnull=False)
            )
        elif conversion == 'not_converted':
            queryset = queryset.filter(
                generated_task__isnull=True,
                generated_recurring_task__isnull=True,
                generated_project_task__isnull=True,
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_task_base_url'] = reverse('task_create')
        context['create_recurring_task_base_url'] = reverse('recurring_task_create')
        context['create_project_task_base_url'] = reverse('project_task_create')
        context['projects'] = Project.objects.order_by('title')
        context['selected_conversion'] = self.request.GET.get('conversion') or 'not_converted'
        context['query_string'] = build_querystring(self.request, exclude={'page'})
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
        default_project = project_services.get_default_project()
        context['default_project_id'] = default_project.pk if default_project else ''
        return context

    def get_initial(self):
        initial = super().get_initial()
        project_id = self.request.GET.get('project')
        possible_task_id = self.request.GET.get('possible_task')
        if possible_task_id:
            possible_task = possible_task_services.get_possible_task(possible_task_id)
            project_id = possible_task.project_id or project_id
        if project_id:
            initial['project'] = project_id
        else:
            default_project = project_services.get_default_project()
            if default_project:
                initial['project'] = default_project.pk
        return initial

    def form_valid(self, form):
        response = super().form_valid(form)
        if is_htmx_request(self.request):
            return htmx_redirect(self.get_success_url())
        return response


class PossibleTaskDetailView(HtmxTemplateMixin, PageTitleMixin, LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.PossibleTask
    template_name = 'possible_task_detail.html'
    htmx_template_name = 'possible_tasks/partials/possible_task_detail_content.html'
    page_title = 'BTY - Possíveis tarefas'
    permission_required = 'possible_tasks.view_possibletask'


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
