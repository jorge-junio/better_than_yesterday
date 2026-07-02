from unittest import mock
from types import SimpleNamespace

from django.template.loader import render_to_string
from django.test import RequestFactory, SimpleTestCase
from django.urls import reverse
from django.utils import timezone

from english_words.models import EnglishWord

from .forms import EvaluationAnswerForm, EvaluationForm, EvaluationItemForm
from .models import Evaluation, EvaluationItem
from .views import EvaluationCreateView, EvaluationListView, EvaluationQuizView


class EvaluationModelTests(SimpleTestCase):
    def test_str_returns_timestamp_label(self):
        evaluation = Evaluation(questions_requested=3)
        self.assertIn('Avaliação', str(evaluation))

    def test_fields_exist(self):
        self.assertEqual(Evaluation._meta.get_field('questions_requested').verbose_name, 'quantidade de perguntas')
        self.assertEqual(EvaluationItem._meta.get_field('answer').verbose_name, 'minha resposta')


class EvaluationFormTests(SimpleTestCase):
    def test_sets_max_value_from_words_count(self):
        with mock.patch('evaluations.forms.get_quizable_words_count', return_value=12):
            form = EvaluationForm()

        self.assertEqual(form.fields['questions_requested'].max_value, 12)


class EvaluationAnswerFormTests(SimpleTestCase):
    def test_answer_field_uses_uppercase_mask(self):
        form = EvaluationAnswerForm()

        self.assertEqual(form.fields['answer'].widget.attrs.get('data-uppercase'), 'true')
        self.assertIn('text-uppercase', form.fields['answer'].widget.attrs.get('class', ''))

    def test_clean_answer_uppercases_text(self):
        form = EvaluationAnswerForm(data={'answer': 'MiXeD CaSe'})

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['answer'], 'MIXED CASE')


class EvaluationItemFormTests(SimpleTestCase):
    def test_answer_field_uses_uppercase_mask(self):
        form = EvaluationItemForm()

        self.assertEqual(form.fields['answer'].widget.attrs.get('data-uppercase'), 'true')
        self.assertIn('text-uppercase', form.fields['answer'].widget.attrs.get('class', ''))

    def test_clean_answer_uppercases_text(self):
        form = EvaluationItemForm()
        form.cleaned_data = {'answer': 'MiXeD CaSe'}

        self.assertEqual(form.clean_answer(), 'MIXED CASE')


class EvaluationUrlTests(SimpleTestCase):
    def test_urls_exist(self):
        self.assertEqual(reverse('evaluation_list'), '/evaluations/list/')
        self.assertEqual(reverse('evaluation_create'), '/evaluations/create/')
        self.assertEqual(reverse('evaluation_detail', args=[1]), '/evaluations/1/detail/')
        self.assertEqual(reverse('evaluation_update', args=[1]), '/evaluations/1/update/')
        self.assertEqual(reverse('evaluation_delete', args=[1]), '/evaluations/1/delete/')


class EvaluationListViewTests(SimpleTestCase):
    def test_view_uses_list_template(self):
        self.assertEqual(EvaluationListView.template_name, 'evaluation_list.html')


class EvaluationListContentTests(SimpleTestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

    def render_template(self, evaluations):
        request = self.request_factory.get('/evaluations/list/')
        request.user = mock.Mock(
            is_authenticated=True,
            has_perm=mock.Mock(return_value=True),
            has_module_perms=mock.Mock(return_value=True),
        )

        return render_to_string(
            'evaluations/partials/evaluation_list_content.html',
            {
                'page_title': 'BTY - Avaliações',
                'evaluations': evaluations,
            },
            request=request,
        )

    def test_renders_continue_quiz_button_for_incomplete_evaluation(self):
        evaluation = SimpleNamespace(
            id=9,
            tested_at=timezone.now(),
            questions_requested=3,
            correct_items_count=2,
            incorrect_items_count=1,
            is_completed=False,
        )

        html = self.render_template([evaluation])

        self.assertIn('Ver resultado', html)
        self.assertIn('/evaluations/9/detail/', html)
        self.assertIn('Continuar quiz', html)
        self.assertIn('/evaluations/9/quiz/', html)
        self.assertIn('Acertos 2', html)
        self.assertIn('Erros 1', html)
        self.assertNotIn('Máx.', html)

    def test_hides_continue_quiz_button_for_completed_evaluation(self):
        evaluation = SimpleNamespace(
            id=9,
            tested_at=timezone.now(),
            questions_requested=3,
            correct_items_count=5,
            incorrect_items_count=0,
            is_completed=True,
        )

        html = self.render_template([evaluation])

        self.assertIn('Ver resultado', html)
        self.assertIn('/evaluations/9/detail/', html)
        self.assertNotIn('Continuar quiz', html)
        self.assertNotIn('/evaluations/9/quiz/', html)
        self.assertIn('Acertos 5', html)
        self.assertIn('Erros 0', html)
        self.assertNotIn('Máx.', html)


class EvaluationDetailContentTests(SimpleTestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

    def render_template(self, evaluation):
        request = self.request_factory.get('/evaluations/3/detail/')
        request.user = mock.Mock(
            is_authenticated=True,
            has_perm=mock.Mock(return_value=True),
            has_module_perms=mock.Mock(return_value=True),
        )

        return render_to_string(
            'evaluations/partials/evaluation_detail_content.html',
            {
                'page_title': 'BTY - Avaliações',
                'object': evaluation,
                'word_return_to_url': '/evaluations/3/detail/',
            },
            request=request,
        )

    def test_renders_word_editor_button_with_return_url(self):
        word = SimpleNamespace(
            id=7,
            word='APPLE',
            meanings_text=['FRUTA', 'MAÇÃ'],
        )
        item = SimpleNamespace(
            word=word,
            is_correct=False,
            answer='BANANA',
        )
        items = SimpleNamespace(all=lambda: [item])
        evaluation = SimpleNamespace(
            id=3,
            tested_at=timezone.now(),
            questions_requested=1,
            answered_items_count=1,
            correct_items_count=0,
            incorrect_items_count=1,
            progress_percentage=100,
            is_completed=True,
            items=items,
        )

        html = self.render_template(evaluation)

        self.assertIn('Editar palavra', html)
        self.assertIn('/english-words/7/update/', html)
        self.assertIn('return_to=/evaluations/3/detail/', html)
        self.assertIn('btn-outline-danger', html)

    def test_renders_success_outline_for_correct_item(self):
        word = SimpleNamespace(
            id=7,
            word='APPLE',
            meanings_text=['FRUTA', 'MAÇÃ'],
        )
        item = SimpleNamespace(
            word=word,
            is_correct=True,
            answer='FRUTA',
        )
        items = SimpleNamespace(all=lambda: [item])
        evaluation = SimpleNamespace(
            id=3,
            tested_at=timezone.now(),
            questions_requested=1,
            answered_items_count=1,
            correct_items_count=1,
            incorrect_items_count=0,
            progress_percentage=100,
            is_completed=True,
            items=items,
        )

        html = self.render_template(evaluation)

        self.assertIn('btn-outline-success', html)


class EvaluationCreateViewTests(SimpleTestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

    def test_form_valid_redirects_to_quiz(self):
        request = self.request_factory.post('/evaluations/create/', {'questions_requested': 3})
        request.user = mock.Mock(is_authenticated=True)

        view = EvaluationCreateView()
        view.request = request

        form = mock.Mock()
        evaluation = mock.Mock(pk=9, questions_requested=3, items=mock.Mock())
        form.save.return_value = evaluation

        response = view.form_valid(form)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/evaluations/9/quiz/')
        evaluation.save.assert_not_called()


class EvaluationQuizViewTests(SimpleTestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

    def test_get_quiz_word_ids_generates_and_persists_sequence(self):
        view = EvaluationQuizView()
        evaluation = mock.Mock(pk=9, questions_requested=3, quiz_word_ids=[], items=mock.Mock())
        evaluation.items.exists.return_value = False
        evaluation.save = mock.Mock()
        view.object = evaluation

        with mock.patch('evaluations.views.build_quiz_word_ids', return_value=[4, 5, 6]):
            word_ids = view.get_quiz_word_ids()

        self.assertEqual(word_ids, [4, 5, 6])
        self.assertEqual(evaluation.quiz_word_ids, [4, 5, 6])
        evaluation.save.assert_called_once_with(update_fields=['quiz_word_ids'])

    def test_form_valid_creates_item_and_redirects_to_report_when_finished(self):
        request = self.request_factory.post('/evaluations/9/quiz/', {'answer': 'APPLE'})
        request.user = mock.Mock(is_authenticated=True)

        view = EvaluationQuizView()
        view.request = request
        evaluation = mock.Mock(pk=9, questions_requested=1, quiz_word_ids=[11], items=mock.Mock())
        evaluation.items.exists.return_value = False
        evaluation.items.count.return_value = 0
        evaluation.is_completed = True
        evaluation.invalidate_items_cache = mock.Mock()
        view.object = evaluation

        current_word = mock.Mock()
        current_word.meanings.all.return_value = [mock.Mock(text='APPLE')]
        view.get_current_word = mock.Mock(return_value=current_word)

        form = EvaluationAnswerForm(data={'answer': 'APPLE'})
        self.assertTrue(form.is_valid())

        with mock.patch('evaluations.views.is_answer_correct', return_value=True), \
             mock.patch('evaluations.views.models.EvaluationItem.objects.create') as create_mock:
            evaluation.items.count.return_value = 1
            response = view.form_valid(form)

        create_mock.assert_called_once_with(
            evaluation=evaluation,
            word=current_word,
            answer='APPLE',
            is_correct=True,
        )
        evaluation.invalidate_items_cache.assert_called_once()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/evaluations/9/detail/')
