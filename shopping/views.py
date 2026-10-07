from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Count, Sum
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django import forms as django_forms

from app.utils import build_querystring, htmx_redirect, is_htmx_request
from . import forms, models, services


def navigate(request, name, **kwargs):
    url = reverse(name, kwargs=kwargs)
    return htmx_redirect(url) if is_htmx_request(request) else redirect(url)


class ShoppingView(LoginRequiredMixin, PermissionRequiredMixin, View):
    page_title = 'BTY - Compras'
    shopping_section = 'lists'

    def display(self, request, partial, context=None):
        context = {'page_title': self.page_title, 'shopping_section': self.shopping_section, 'content_template': f'shopping/partials/{partial}.html', **(context or {})}
        return render(request, context['content_template'] if is_htmx_request(request) else 'shopping/page.html', context)


class ListView(ShoppingView):
    permission_required = 'shopping.view_shoppinglist'

    def get(self, request):
        queryset = models.ShoppingList.objects.filter(owner=request.user).annotate(item_count=Count('items')).order_by('name', 'id')
        page = Paginator(queryset, 20).get_page(request.GET.get('page'))
        return self.display(request, 'lists', {'lists': page, 'page_obj': page})


class ListDetailView(ShoppingView):
    permission_required = 'shopping.view_shoppinglist'

    def get(self, request, pk):
        shopping_list = get_object_or_404(models.ShoppingList, pk=pk, owner=request.user)
        return self.display(request, 'list_detail', {'shopping_list': shopping_list, 'items': shopping_list.items.all()})


class ListFormView(ShoppingView):
    def get_permission_required(self):
        return ('shopping.change_shoppinglist' if self.kwargs.get('pk') else 'shopping.add_shoppinglist',)

    def get_instance(self, request, pk):
        return get_object_or_404(models.ShoppingList, pk=pk, owner=request.user) if pk else models.ShoppingList(owner=request.user)

    def display_form(self, request, form):
        return self.display(request, 'form', {'form': form, 'heading': 'Editar lista de compras' if form.instance.pk else 'Nova lista de compras', 'submit_label': 'Salvar lista', 'cancel_url': reverse('shopping_list_detail', args=[form.instance.pk]) if form.instance.pk else reverse('shopping_list')})

    def get(self, request, pk=None):
        return self.display_form(request, forms.ShoppingListForm(instance=self.get_instance(request, pk)))

    def post(self, request, pk=None):
        form = forms.ShoppingListForm(request.POST, instance=self.get_instance(request, pk))
        if form.is_valid():
            with transaction.atomic():
                if pk:
                    get_object_or_404(models.ShoppingList.objects.select_for_update(), pk=pk, owner=request.user)
                shopping_list = form.save()
            return navigate(request, 'shopping_list_detail', pk=shopping_list.pk)
        return self.display_form(request, form)


class ItemFormView(ShoppingView):
    def get_permission_required(self):
        return ('shopping.change_shoppingitem' if self.kwargs.get('item_id') else 'shopping.add_shoppingitem',)

    def get_instance(self, request, list_id, item_id):
        shopping_list = get_object_or_404(models.ShoppingList, pk=list_id, owner=request.user)
        return get_object_or_404(models.ShoppingItem, pk=item_id, shopping_list=shopping_list) if item_id else models.ShoppingItem(shopping_list=shopping_list)

    def display_form(self, request, form, list_id):
        return self.display(request, 'form', {'form': form, 'heading': 'Editar item da feira' if form.instance.pk else 'Adicionar item da feira', 'submit_label': 'Salvar item', 'cancel_url': reverse('shopping_list_detail', args=[list_id])})

    def get(self, request, list_id, item_id=None):
        return self.display_form(request, forms.ShoppingItemForm(instance=self.get_instance(request, list_id, item_id)), list_id)

    def post(self, request, list_id, item_id=None):
        form = forms.ShoppingItemForm(request.POST, instance=self.get_instance(request, list_id, item_id))
        if form.is_valid():
            try:
                with transaction.atomic():
                    get_object_or_404(models.ShoppingList.objects.select_for_update(), pk=list_id, owner=request.user)
                    form.instance.full_clean()
                    form.save()
                return navigate(request, 'shopping_list_detail', pk=list_id)
            except ValidationError as exc:
                form.add_error(None, 'Não foi possível salvar o item. Verifique se já existe outro com o mesmo nome.' if hasattr(exc, 'message_dict') else exc)
        return self.display_form(request, form, list_id)


class StartView(ShoppingView):
    permission_required = ('shopping.view_shoppinglist', 'shopping.view_shoppingsession')
    shopping_section = 'start'
    page_title = 'BTY - Fazer feira'

    def display_selection(self, request, choose_form, selected=None, selection_form=None):
        active_items = selected.items.filter(is_active=True) if selected else models.ShoppingItem.objects.none()
        if selected and selection_form is None:
            selection_form = forms.ItemSelectionForm(shopping_list=selected)
        current = models.ShoppingSession.objects.filter(owner=request.user, status=models.ShoppingSession.Status.IN_PROGRESS).first()
        return self.display(request, 'start', {'choose_form': choose_form, 'selected': selected, 'selection_form': selection_form, 'has_items': active_items.exists(), 'current_session': current})

    def get(self, request):
        choose_form = forms.ChooseListForm(request.GET or None, owner=request.user)
        selected = choose_form.cleaned_data['shopping_list'] if choose_form.is_bound and choose_form.is_valid() else None
        return self.display_selection(request, choose_form, selected)

    def post(self, request):
        if not request.user.has_perm('shopping.add_shoppingsession'):
            self.handle_no_permission()
        choose_form = forms.ChooseListForm(request.POST, owner=request.user)
        if not choose_form.is_valid():
            return self.display_selection(request, choose_form)
        selected = choose_form.cleaned_data['shopping_list']
        selection_form = forms.ItemSelectionForm(request.POST, shopping_list=selected)
        if selection_form.is_valid():
            try:
                session = services.start_session(request.user, selected.pk, [item.pk for item in selection_form.cleaned_data['items']])
                return navigate(request, 'shopping_session', pk=session.pk)
            except ValidationError as exc:
                selection_form.add_error(None, exc)
        return self.display_selection(request, choose_form, selected, selection_form)


class SessionView(ShoppingView):
    permission_required = 'shopping.view_shoppingsession'
    shopping_section = 'start'

    def get_session(self, request, pk):
        return get_object_or_404(models.ShoppingSession.objects.prefetch_related('items'), pk=pk, owner=request.user)

    def display_session(self, request, session, form=None, saved=False):
        editable = session.status == models.ShoppingSession.Status.IN_PROGRESS
        if not editable:
            self.shopping_section = 'history'
        form = form or forms.QuantityForm(items=session.items.all())
        return self.display(request, 'session', {'session': session, 'editable': editable, 'form': form, 'saved': saved})

    def get(self, request, pk):
        return self.display_session(request, self.get_session(request, pk))

    def post(self, request, pk):
        if not request.user.has_perm('shopping.change_shoppingsession'):
            self.handle_no_permission()
        session = self.get_session(request, pk)
        if session.status != models.ShoppingSession.Status.IN_PROGRESS:
            return HttpResponseBadRequest('Esta compra já foi encerrada.')
        action = request.POST.get('action')
        if action not in ['save', 'finish']:
            return HttpResponseBadRequest('Ação inválida.')
        form = forms.QuantityForm(request.POST, items=session.items.all())
        if form.is_valid():
            try:
                services.save_quantities(request.user, pk, {item.pk: form.cleaned_data[f'quantity_{item.pk}'] for item in session.items.all()})
                if action == 'finish':
                    services.validate_ready(session)
                    return navigate(request, 'shopping_finish', pk=pk)
                return navigate(request, 'shopping_session', pk=pk) if not is_htmx_request(request) else self.display_session(request, self.get_session(request, pk), saved=True)
            except ValidationError as exc:
                form.add_error(None, exc)
        return self.display_session(request, session, form)


class FinishView(ShoppingView):
    permission_required = ('shopping.view_shoppingsession', 'shopping.change_shoppingsession')
    shopping_section = 'start'

    def display_form(self, request, session, form):
        return self.display(request, 'finish', {'session': session, 'form': form})

    def get(self, request, pk):
        session = get_object_or_404(models.ShoppingSession, pk=pk, owner=request.user)
        if session.status != models.ShoppingSession.Status.IN_PROGRESS:
            return navigate(request, 'shopping_session', pk=pk)
        try:
            services.validate_ready(session)
        except ValidationError:
            return navigate(request, 'shopping_session', pk=pk)
        return self.display_form(request, session, forms.FinishForm())

    def post(self, request, pk):
        session = get_object_or_404(models.ShoppingSession, pk=pk, owner=request.user)
        form = forms.FinishForm(request.POST)
        if form.is_valid():
            try:
                services.finish_session(request.user, pk, form.cleaned_data['total'])
                return navigate(request, 'shopping_session', pk=pk)
            except ValidationError as exc:
                form.add_error(None, exc)
        return self.display_form(request, session, form)


class CancelView(ShoppingView):
    permission_required = ('shopping.view_shoppingsession', 'shopping.change_shoppingsession')
    shopping_section = 'start'

    def get(self, request, pk):
        session = get_object_or_404(models.ShoppingSession, pk=pk, owner=request.user, status=models.ShoppingSession.Status.IN_PROGRESS)
        return self.display(request, 'form', {'heading': 'Cancelar esta compra?', 'description': f'A compra da lista “{session.list_name}” será encerrada como cancelada. Você poderá iniciar outra feira.', 'submit_label': 'Confirmar cancelamento', 'cancel_url': reverse('shopping_session', args=[pk])})

    def post(self, request, pk):
        services.cancel_session(request.user, pk)
        return navigate(request, 'shopping_history')


class HistoryFilterForm(django_forms.Form):
    start = django_forms.DateField(label='Data inicial', required=False, widget=django_forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'))
    end = django_forms.DateField(label='Data final', required=False, widget=django_forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'))

    def clean(self):
        data = super().clean()
        if data.get('start') and data.get('end') and data['end'] < data['start']:
            raise django_forms.ValidationError('A data final deve ser igual ou posterior à inicial.')
        return data


class HistoryView(ShoppingView):
    permission_required = 'shopping.view_shoppingsession'
    shopping_section = 'history'
    page_title = 'BTY - Histórico de compras'

    def get(self, request):
        queryset = models.ShoppingSession.objects.filter(owner=request.user).exclude(status=models.ShoppingSession.Status.IN_PROGRESS)
        filter_form = HistoryFilterForm(request.GET)
        if filter_form.is_valid():
            if filter_form.cleaned_data.get('start'):
                queryset = queryset.filter(finished_at__date__gte=filter_form.cleaned_data['start'])
            if filter_form.cleaned_data.get('end'):
                queryset = queryset.filter(finished_at__date__lte=filter_form.cleaned_data['end'])
        else:
            queryset = queryset.none()
        completed = queryset.filter(status=models.ShoppingSession.Status.COMPLETED)
        total = completed.aggregate(total=Sum('total'))['total'] or 0
        page = Paginator(queryset, 20).get_page(request.GET.get('page'))
        return self.display(request, 'history', {'sessions': page, 'page_obj': page, 'filter_form': filter_form, 'total': total, 'completed_count': completed.count(), 'query_string': build_querystring(request, exclude={'page'})})
