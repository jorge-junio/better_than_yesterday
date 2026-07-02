import csv
import re
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import connection, transaction
from django_tenants.utils import get_public_schema_name

from english_words.models import EnglishMeaning, EnglishWord


class Command(BaseCommand):
    help = 'Importa palavras e traduções do arquivo docs/palavras.csv no schema atual.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv-path',
            default=None,
            help='Caminho do arquivo CSV. Padrão: docs/palavras.csv',
        )
        parser.add_argument(
            '--replace',
            action='store_true',
            help='Substitui os significados existentes das palavras encontradas no CSV.',
        )

    def handle(self, *args, **options):
        if connection.schema_name == get_public_schema_name():
            raise CommandError(
                'Execute este comando dentro de um schema de tenant, por exemplo com '
                '`tenant_command import_english_words_from_csv -s jjsistemas`.'
            )

        csv_path = Path(options['csv_path']) if options['csv_path'] else Path(__file__).resolve().parents[3] / 'docs' / 'palavras.csv'
        if not csv_path.exists():
            raise CommandError(f'Arquivo não encontrado: {csv_path}')

        records = self.load_records(csv_path)
        stats = self.import_records(records, replace=options['replace'])

        self.stdout.write(
            self.style.SUCCESS(
                (
                    f'Importação concluída em "{connection.schema_name}". '
                    f'Palavras novas: {stats["created_words"]}. '
                    f'Significados novos: {stats["created_meanings"]}. '
                    f'Palavras atualizadas: {stats["updated_words"]}.'
                )
            )
        )

    def load_records(self, csv_path):
        records = {}
        with csv_path.open(encoding='utf-8-sig', newline='') as handle:
            reader = csv.DictReader(handle)
            if not reader.fieldnames:
                raise CommandError('O CSV não possui cabeçalho.')

            expected_headers = {'Palavra', 'Significado'}
            normalized_headers = {header.strip() for header in reader.fieldnames if header}
            if normalized_headers != expected_headers:
                raise CommandError(
                    'O CSV precisa ter exatamente as colunas "Palavra" e "Significado".'
                )

            for row in reader:
                raw_word = (row.get('Palavra') or '').strip()
                raw_meaning = (row.get('Significado') or '').strip()
                if not raw_word or not raw_meaning:
                    continue

                word, note = self.normalize_word_and_note(raw_word)
                meaning = self.normalize_text(raw_meaning)
                if not word or not meaning:
                    continue

                entry = records.setdefault(word, {'note': note, 'meanings': []})
                if note and not entry['note']:
                    entry['note'] = note
                if meaning not in entry['meanings']:
                    entry['meanings'].append(meaning)

        return records

    def normalize_text(self, value):
        return re.sub(r'\s+', ' ', value).strip().upper()

    def normalize_word_and_note(self, raw_word):
        cleaned = re.sub(r'\s+', ' ', raw_word).strip()
        quoted_note_match = re.match(r'^"([^"]+)"\s+(.+)$', cleaned)
        if quoted_note_match:
            note = self.normalize_text(quoted_note_match.group(1))
            word = self.normalize_text(quoted_note_match.group(2))
            return word, note

        return self.normalize_text(cleaned.replace('"', '')), ''

    def import_records(self, records, replace=False):
        stats = {
            'created_words': 0,
            'created_meanings': 0,
            'updated_words': 0,
        }

        existing_words = {
            word.word.upper(): word
            for word in EnglishWord.objects.prefetch_related('meanings')
        }

        with transaction.atomic():
            for word_name, entry in records.items():
                word = existing_words.get(word_name)

                if word is None:
                    word = EnglishWord.objects.create(
                        word=word_name,
                        note=entry['note'],
                    )
                    existing_words[word_name] = word
                    stats['created_words'] += 1
                else:
                    updated_fields = []
                    if word.word != word_name:
                        word.word = word_name
                        updated_fields.append('word')
                    if entry['note'] and not word.note:
                        word.note = entry['note']
                        updated_fields.append('note')
                    if updated_fields:
                        word.save(update_fields=updated_fields)
                        stats['updated_words'] += 1

                if replace:
                    word.meanings.all().delete()
                    existing_meanings = set()
                else:
                    existing_meanings = {
                        meaning.strip().upper()
                        for meaning in word.meanings.values_list('text', flat=True)
                    }

                for meaning in entry['meanings']:
                    if meaning in existing_meanings:
                        continue
                    EnglishMeaning.objects.create(word=word, text=meaning)
                    existing_meanings.add(meaning)
                    stats['created_meanings'] += 1

        return stats
