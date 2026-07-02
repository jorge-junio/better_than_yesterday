import random

from english_words.models import EnglishWord


def get_quizable_words_queryset():
    return EnglishWord.objects.filter(meanings__isnull=False).distinct().order_by('word', 'id')


def get_quizable_words_count():
    return get_quizable_words_queryset().count()


def build_quiz_word_ids(quantity):
    word_ids = list(get_quizable_words_queryset().values_list('id', flat=True))
    random.shuffle(word_ids)
    return word_ids[:quantity]


def get_words_for_quiz(word_ids):
    if not word_ids:
        return []

    words = EnglishWord.objects.filter(id__in=word_ids).prefetch_related('meanings')
    word_map = {word.id: word for word in words}
    return [word_map[word_id] for word_id in word_ids if word_id in word_map]


def normalize_quiz_answer(value):
    return (value or '').strip().upper()


def is_answer_correct(word, answer):
    normalized_answer = normalize_quiz_answer(answer)
    expected_answers = {
        normalize_quiz_answer(meaning.text)
        for meaning in word.meanings.all()
    }
    return normalized_answer in expected_answers
