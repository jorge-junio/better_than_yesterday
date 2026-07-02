from unittest import mock

from django.test import RequestFactory, SimpleTestCase
from django.urls import reverse

from .forms import EnglishWordEditorForm, EnglishWordLookupForm
from .models import EnglishMeaning, EnglishWord
from .views import EnglishWordCreateView, EnglishWordUpdateView


class EnglishWordModelTests(SimpleTestCase):
    def test_str_returns_word(self):
        english_word = EnglishWord(word='apple')

        self.assertEqual(str(english_word), 'apple')

    def test_fields_exist(self):
        self.assertEqual(EnglishWord._meta.get_field('word').verbose_name, 'palavra')
        self.assertEqual(EnglishWord._meta.get_field('note').verbose_name, 'observação')

    def test_meanings_relation_exists(self):
        field = EnglishWord._meta.get_field('meanings')
        self.assertEqual(field.related_model.__name__, 'EnglishMeaning')

class EnglishWordFormTests(SimpleTestCase):
    def test_lookup_form_has_only_word_field(self):
        form = EnglishWordLookupForm()

        self.assertEqual(list(form.fields.keys()), ['word'])
        self.assertEqual(form.fields['word'].widget.attrs.get('data-uppercase'), 'true')
        self.assertIn('text-uppercase', form.fields['word'].widget.attrs.get('class', ''))

    def test_lookup_form_uppercases_word(self):
        form = EnglishWordLookupForm(data={'word': 'ApPlE'})

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['word'], 'APPLE')

    def test_editor_form_has_expected_fields(self):
        form = EnglishWordEditorForm()

        self.assertEqual(list(form.fields.keys()), ['word', 'note'])
        self.assertEqual(form.fields['word'].widget.attrs.get('readonly'), 'readonly')
        self.assertNotIn('meanings', form.fields)
        self.assertEqual(form.fields['word'].widget.attrs.get('data-uppercase'), 'true')
        self.assertEqual(form.fields['note'].widget.attrs.get('data-uppercase'), 'true')
        self.assertIn('text-uppercase', form.fields['word'].widget.attrs.get('class', ''))
        self.assertIn('text-uppercase', form.fields['note'].widget.attrs.get('class', ''))

    def test_editor_form_uppercases_meanings(self):
        self.assertEqual(
            EnglishWordEditorForm.normalize_meanings([' apple ', '', ' Fruta  ']),
            ['APPLE', 'FRUTA'],
        )

    def test_editor_form_uppercases_note_and_word(self):
        form = EnglishWordEditorForm(data={'word': 'ApPlE', 'note': 'MiXeD CaSe'}, word_locked=False)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['word'], 'APPLE')
        self.assertEqual(form.cleaned_data['note'], 'MIXED CASE')


class EnglishWordCreateViewTests(SimpleTestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

    def test_get_form_class_switches_by_query_string(self):
        lookup_request = self.request_factory.get('/english-words/create/')
        lookup_request.user = mock.Mock(is_authenticated=True)
        lookup_view = EnglishWordCreateView()
        lookup_view.request = lookup_request

        editor_request = self.request_factory.get('/english-words/create/?word=apple')
        editor_request.user = mock.Mock(is_authenticated=True)
        editor_view = EnglishWordCreateView()
        editor_view.request = editor_request

        self.assertIs(lookup_view.get_form_class(), EnglishWordLookupForm)
        self.assertIs(editor_view.get_form_class(), EnglishWordEditorForm)

    def test_get_form_kwargs_removes_instance_in_lookup_mode(self):
        request = self.request_factory.get('/english-words/create/')
        request.user = mock.Mock(is_authenticated=True)
        view = EnglishWordCreateView()
        view.request = request
        view.object = None

        kwargs = view.get_form_kwargs()

        self.assertNotIn('instance', kwargs)

    def test_proceed_to_editor_redirects_to_update_when_word_exists(self):
        request = self.request_factory.post('/english-words/create/?return_to=/evaluations/3/detail/', {'word': 'apple'})
        request.user = mock.Mock(is_authenticated=True)
        view = EnglishWordCreateView()
        view.request = request

        form = mock.Mock()
        form.is_valid.return_value = True
        form.cleaned_data = {'word': 'APPLE'}
        view.get_form = mock.Mock(return_value=form)

        existing = mock.Mock(pk=7)
        with mock.patch('english_words.views.models.EnglishWord.objects.filter') as filter_mock:
            filter_mock.return_value.first.return_value = existing
            response = view.proceed_to_editor()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/english-words/7/update/?return_to=%2Fevaluations%2F3%2Fdetail%2F')

    def test_proceed_to_editor_redirects_back_to_create_when_word_is_new(self):
        request = self.request_factory.post('/english-words/create/?return_to=/evaluations/3/detail/', {'word': 'apple'})
        request.user = mock.Mock(is_authenticated=True)
        view = EnglishWordCreateView()
        view.request = request

        form = mock.Mock()
        form.is_valid.return_value = True
        form.cleaned_data = {'word': 'APPLE'}
        view.get_form = mock.Mock(return_value=form)

        with mock.patch('english_words.views.models.EnglishWord.objects.filter') as filter_mock:
            filter_mock.return_value.first.return_value = None
            response = view.proceed_to_editor()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/english-words/create/?word=APPLE&return_to=%2Fevaluations%2F3%2Fdetail%2F')

    def test_proceed_to_editor_normalizes_word_before_redirect(self):
        request = self.request_factory.post('/english-words/create/', {'word': 'ApPlE'})
        request.user = mock.Mock(is_authenticated=True)
        view = EnglishWordCreateView()
        view.request = request

        form = mock.Mock()
        form.is_valid.return_value = True
        form.cleaned_data = {'word': 'APPLE'}
        view.get_form = mock.Mock(return_value=form)

        with mock.patch('english_words.views.models.EnglishWord.objects.filter') as filter_mock:
            filter_mock.return_value.first.return_value = None
            response = view.proceed_to_editor()

        self.assertEqual(response.url, '/english-words/create/?word=APPLE')


class EnglishWordUpdateViewTests(SimpleTestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

    def test_get_cancel_url_uses_return_to_when_present(self):
        request = self.request_factory.get('/english-words/7/update/?return_to=/evaluations/3/detail/')
        request.user = mock.Mock(is_authenticated=True)

        view = EnglishWordUpdateView()
        view.request = request

        self.assertEqual(view.get_cancel_url(), '/evaluations/3/detail/')

    def test_get_success_url_uses_return_to_when_present(self):
        request = self.request_factory.get('/english-words/7/update/?return_to=/evaluations/3/detail/')
        request.user = mock.Mock(is_authenticated=True)

        view = EnglishWordUpdateView()
        view.request = request

        self.assertEqual(view.get_success_url(), '/evaluations/3/detail/')


class EnglishWordUrlTests(SimpleTestCase):
    def test_urls_exist(self):
        self.assertEqual(reverse('english_word_list'), '/english-words/list/')
        self.assertEqual(reverse('english_word_create'), '/english-words/create/')
        self.assertEqual(reverse('english_word_detail', args=[1]), '/english-words/1/detail/')
        self.assertEqual(reverse('english_word_update', args=[1]), '/english-words/1/update/')
        self.assertEqual(reverse('english_word_delete', args=[1]), '/english-words/1/delete/')
