from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from urllib.parse import urlencode

from app.utils import HtmxTemplateMixin, PageTitleMixin, htmx_redirect, is_htmx_request

from . import forms, models


def get_safe_return_to_url(request):
    return_to = request.GET.get('return_to') or request.POST.get('return_to')
    if return_to and url_has_allowed_host_and_scheme(
        return_to,
        allowed_hosts=set(),
        require_https=request.is_secure(),
    ):
        return return_to
    return None


def append_query_params(url, params):
    query_params = {key: value for key, value in params.items() if value}
    if not query_params:
        return url
    return f'{url}?{urlencode(query_params)}'


class EnglishWordListView(HtmxTemplateMixin, PageTitleMixin, LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.EnglishWord
    template_name = 'english_word_list.html'
    htmx_template_name = 'english_words/partials/english_word_list_content.html'
    page_title = 'BTY - Palavras em inglês'
    context_object_name = 'english_words'
    paginate_by = 20
    permission_required = 'english_words.view_englishword'


class EnglishWordCreateView(HtmxTemplateMixin, PageTitleMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.EnglishWord
    template_name = 'english_word_create.html'
    htmx_template_name = 'english_words/partials/english_word_form_content.html'
    page_title = 'BTY - Nova palavra em inglês'
    success_url = reverse_lazy('english_word_list')
    permission_required = 'english_words.add_englishword'

    def get_return_to_url(self):
        return get_safe_return_to_url(self.request)

    def get_cancel_url(self):
        return self.get_return_to_url() or reverse_lazy('english_word_list')

    def get_success_url(self):
        return self.get_return_to_url() or super().get_success_url()

    def get_form_class(self):
        if self.request.GET.get('word'):
            return forms.EnglishWordEditorForm
        return forms.EnglishWordLookupForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.GET.get('word'):
            kwargs['word_locked'] = True
        else:
            kwargs.pop('instance', None)
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        word = (self.request.GET.get('word') or '').strip().upper()
        if word:
            initial['word'] = word
            instance = models.EnglishWord.objects.filter(word__iexact=word).first()
            if instance:
                initial['note'] = instance.note
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        editor_mode = bool(self.request.GET.get('word'))
        context['editor_mode'] = editor_mode
        context['page_heading'] = 'Cadastrar Palavra em Inglês'
        context['submit_label'] = 'Prosseguir' if not editor_mode else 'Salvar palavra'
        context['cancel_url'] = self.get_cancel_url()
        context['meanings_values'] = []
        if editor_mode:
            word = (self.request.GET.get('word') or '').strip().upper()
            context['meanings_values'] = list(
                models.EnglishMeaning.objects.filter(word__word__iexact=word).order_by('id').values_list('text', flat=True)
            ) if models.EnglishMeaning.objects.filter(word__word__iexact=word).exists() else ['']
            if not context['meanings_values']:
                context['meanings_values'] = ['']
            context['word_locked'] = True
        return context

    def post(self, request, *args, **kwargs):
        if request.GET.get('word'):
            return self.save_word()
        return self.proceed_to_editor()

    def proceed_to_editor(self):
        form = self.get_form()
        if not form.is_valid():
            return self.form_invalid(form)

        word = form.cleaned_data['word'].strip().upper()
        existing = models.EnglishWord.objects.filter(word__iexact=word).first()
        return_to_url = self.get_return_to_url()
        if existing:
            return redirect(
                append_query_params(reverse('english_word_update', args=[existing.pk]), {'return_to': return_to_url})
            )
        return redirect(
            append_query_params(
                reverse('english_word_create'),
                {
                    'word': word,
                    'return_to': return_to_url,
                },
            )
        )

    def save_word(self):
        form = self.get_form()
        if not form.is_valid():
            return self.form_invalid(form)

        meanings = self.request.POST.getlist('meanings')
        cleaned_meanings = forms.EnglishWordEditorForm.normalize_meanings(meanings)
        if not cleaned_meanings:
            form.add_error(None, 'Adicione pelo menos um significado.')
            return self.form_invalid(form)
        instance = form.save(commit=False)
        instance.word = (self.request.GET.get('word') or instance.word).strip().upper()
        instance.save()
        form.save_m2m()
        form.save_meanings(instance, cleaned_meanings)
        self.object = instance
        if is_htmx_request(self.request):
            return htmx_redirect(self.get_success_url())
        return redirect(self.get_success_url())

    def form_valid(self, form):
        if self.request.GET.get('word'):
            return self.save_word()
        return self.proceed_to_editor()


class EnglishWordDetailView(HtmxTemplateMixin, PageTitleMixin, LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.EnglishWord
    template_name = 'english_word_detail.html'
    htmx_template_name = 'english_words/partials/english_word_detail_content.html'
    page_title = 'BTY - Palavras em inglês'
    permission_required = 'english_words.view_englishword'


class EnglishWordUpdateView(HtmxTemplateMixin, PageTitleMixin, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.EnglishWord
    template_name = 'english_word_update.html'
    htmx_template_name = 'english_words/partials/english_word_form_content.html'
    page_title = 'BTY - Editar palavra em inglês'
    form_class = forms.EnglishWordEditorForm
    success_url = reverse_lazy('english_word_list')
    permission_required = 'english_words.change_englishword'

    def get_return_to_url(self):
        return get_safe_return_to_url(self.request)

    def get_cancel_url(self):
        return self.get_return_to_url() or reverse_lazy('english_word_list')

    def get_success_url(self):
        return self.get_return_to_url() or super().get_success_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_heading'] = 'Editar Palavra em Inglês'
        context['submit_label'] = 'Salvar palavra'
        context['cancel_url'] = self.get_cancel_url()
        context['editor_mode'] = True
        context['word_locked'] = True
        context['meanings_values'] = list(self.object.meanings.order_by('id').values_list('text', flat=True)) or ['']
        return context

    def form_valid(self, form):
        meanings = self.request.POST.getlist('meanings')
        cleaned_meanings = forms.EnglishWordEditorForm.normalize_meanings(meanings)
        if not cleaned_meanings:
            form.add_error(None, 'Adicione pelo menos um significado.')
            return self.form_invalid(form)
        response = super().form_valid(form)
        form.save_meanings(self.object, cleaned_meanings)
        if is_htmx_request(self.request):
            return htmx_redirect(self.get_success_url())
        return response


class EnglishWordDeleteView(HtmxTemplateMixin, PageTitleMixin, LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.EnglishWord
    template_name = 'english_word_delete.html'
    htmx_template_name = 'english_words/partials/english_word_delete_content.html'
    page_title = 'BTY - Excluir palavra em inglês'
    success_url = reverse_lazy('english_word_list')
    permission_required = 'english_words.delete_englishword'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('english_word_list')
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        if is_htmx_request(request):
            return htmx_redirect(success_url)
        return redirect(success_url)
