from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from app.utils import HtmxTemplateMixin, PageTitleMixin, htmx_redirect, is_htmx_request

from . import forms, models


class CategoryListView(HtmxTemplateMixin, PageTitleMixin, LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.Category
    template_name = 'category_list.html'
    htmx_template_name = 'categories/partials/category_list_content.html'
    page_title = 'BTY - Categorias'
    context_object_name = 'categories'
    paginate_by = 20
    permission_required = 'categories.view_category'


class CategoryCreateView(HtmxTemplateMixin, PageTitleMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Category
    template_name = 'category_create.html'
    htmx_template_name = 'categories/partials/category_form_content.html'
    page_title = 'BTY - Nova Categoria'
    form_class = forms.CategoryForm
    success_url = reverse_lazy('category_list')
    permission_required = 'categories.add_category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_heading'] = 'Cadastrar Categoria'
        context['submit_label'] = 'Salvar categoria'
        context['cancel_url'] = reverse_lazy('category_list')
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        if is_htmx_request(self.request):
            return htmx_redirect(self.get_success_url())
        return response


class CategoryUpdateView(HtmxTemplateMixin, PageTitleMixin, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.Category
    template_name = 'category_update.html'
    htmx_template_name = 'categories/partials/category_form_content.html'
    page_title = 'BTY - Editar Categoria'
    form_class = forms.CategoryForm
    success_url = reverse_lazy('category_list')
    permission_required = 'categories.change_category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_heading'] = 'Editar Categoria'
        context['submit_label'] = 'Salvar categoria'
        context['cancel_url'] = reverse_lazy('category_list')
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        if is_htmx_request(self.request):
            return htmx_redirect(self.get_success_url())
        return response


class CategoryDeleteView(HtmxTemplateMixin, PageTitleMixin, LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Category
    template_name = 'category_delete.html'
    htmx_template_name = 'categories/partials/category_delete_content.html'
    page_title = 'BTY - Excluir Categoria'
    success_url = reverse_lazy('category_list')
    permission_required = 'categories.delete_category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('category_list')
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        if is_htmx_request(request):
            return htmx_redirect(success_url)
        return redirect(success_url)

