from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, FormView, ListView, UpdateView

from app.utils import HtmxTemplateMixin, PageTitleMixin, htmx_redirect, is_htmx_request

from . import forms, models
from .services import build_quiz_word_ids, get_words_for_quiz, is_answer_correct


class EvaluationListView(HtmxTemplateMixin, PageTitleMixin, LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.Evaluation
    template_name = 'evaluation_list.html'
    htmx_template_name = 'evaluations/partials/evaluation_list_content.html'
    page_title = 'BTY - Avaliações'
    context_object_name = 'evaluations'
    paginate_by = 20
    permission_required = 'evaluations.view_evaluation'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('items')


class EvaluationCreateView(HtmxTemplateMixin, PageTitleMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Evaluation
    template_name = 'evaluation_create.html'
    htmx_template_name = 'evaluations/partials/evaluation_form_content.html'
    page_title = 'BTY - Nova avaliação'
    form_class = forms.EvaluationForm
    success_url = reverse_lazy('evaluation_list')
    permission_required = 'evaluations.add_evaluation'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_heading'] = 'Cadastrar Avaliação'
        context['submit_label'] = 'Salvar avaliação'
        context['cancel_url'] = reverse_lazy('evaluation_list')
        return context

    def form_valid(self, form):
        self.object = form.save()
        next_url = reverse('evaluation_quiz', args=[self.object.pk])
        if is_htmx_request(self.request):
            return htmx_redirect(next_url)
        return redirect(next_url)


class EvaluationDetailView(HtmxTemplateMixin, PageTitleMixin, LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Evaluation
    template_name = 'evaluation_detail.html'
    htmx_template_name = 'evaluations/partials/evaluation_detail_content.html'
    page_title = 'BTY - Avaliações'
    permission_required = 'evaluations.view_evaluation'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('items__word__meanings', 'items__word')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['word_return_to_url'] = self.request.get_full_path()
        return context


class EvaluationQuizView(HtmxTemplateMixin, PageTitleMixin, LoginRequiredMixin, PermissionRequiredMixin, FormView):
    model = models.Evaluation
    template_name = 'evaluation_quiz.html'
    htmx_template_name = 'evaluations/partials/evaluation_quiz_content.html'
    page_title = 'BTY - Quiz de vocabulário'
    form_class = forms.EvaluationAnswerForm
    permission_required = 'evaluations.add_evaluation'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_completed:
            return redirect('evaluation_detail', pk=self.object.pk)
        if self.get_current_word() is None:
            return redirect('evaluation_detail', pk=self.object.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        if not hasattr(self, '_object'):
            self._object = get_object_or_404(models.Evaluation, pk=self.kwargs['pk'])
        return self._object

    def get_quiz_word_ids(self):
        word_ids = list(self.object.quiz_word_ids or [])
        if word_ids:
            return word_ids

        if self.object.items.exists():
            return word_ids

        word_ids = build_quiz_word_ids(self.object.questions_requested)
        self.object.quiz_word_ids = word_ids
        self.object.save(update_fields=['quiz_word_ids'])
        return word_ids

    def get_quiz_words(self):
        return get_words_for_quiz(self.get_quiz_word_ids())

    def get_current_word(self):
        words = self.get_quiz_words()
        current_index = self.object.answered_items_count
        if current_index >= len(words):
            return None
        return words[current_index]

    def get_total_questions(self):
        return len(self.get_quiz_word_ids())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_word = self.get_current_word()
        if current_word is None:
            return context

        context['evaluation'] = self.object
        context['current_word'] = current_word
        context['question_number'] = self.object.answered_items_count + 1
        context['total_questions'] = self.get_total_questions()
        context['progress_percentage'] = self.object.progress_percentage
        context['cancel_url'] = reverse_lazy('evaluation_list')
        context['report_url'] = reverse('evaluation_detail', args=[self.object.pk])
        return context

    def get_success_url(self):
        if self.object.is_completed:
            return reverse('evaluation_detail', args=[self.object.pk])
        return reverse('evaluation_quiz', args=[self.object.pk])

    def form_valid(self, form):
        current_word = self.get_current_word()
        if current_word is None:
            return redirect(self.get_success_url())

        answer = form.cleaned_data['answer']
        models.EvaluationItem.objects.create(
            evaluation=self.object,
            word=current_word,
            answer=answer,
            is_correct=is_answer_correct(current_word, answer),
        )
        self.object.invalidate_items_cache()
        next_url = self.get_success_url()
        if is_htmx_request(self.request):
            return htmx_redirect(next_url)
        return redirect(next_url)


class EvaluationUpdateView(HtmxTemplateMixin, PageTitleMixin, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.Evaluation
    template_name = 'evaluation_update.html'
    htmx_template_name = 'evaluations/partials/evaluation_form_content.html'
    page_title = 'BTY - Editar avaliação'
    form_class = forms.EvaluationForm
    success_url = reverse_lazy('evaluation_list')
    permission_required = 'evaluations.change_evaluation'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_heading'] = 'Editar Avaliação'
        context['submit_label'] = 'Salvar avaliação'
        context['cancel_url'] = reverse_lazy('evaluation_list')
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        if is_htmx_request(self.request):
            return htmx_redirect(self.get_success_url())
        return response


class EvaluationDeleteView(HtmxTemplateMixin, PageTitleMixin, LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Evaluation
    template_name = 'evaluation_delete.html'
    htmx_template_name = 'evaluations/partials/evaluation_delete_content.html'
    page_title = 'BTY - Excluir avaliação'
    success_url = reverse_lazy('evaluation_list')
    permission_required = 'evaluations.delete_evaluation'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('evaluation_list')
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        if is_htmx_request(request):
            return htmx_redirect(success_url)
        return redirect(success_url)
