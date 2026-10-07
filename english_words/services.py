import csv
import io
import json

from django.core.exceptions import ValidationError
from django.db import transaction

from .models import EnglishMeaning, EnglishWord


MAX_IMPORT_SIZE = 5 * 1024 * 1024


def parse_word_import(upload):
    extension = upload.name.rsplit('.', 1)[-1].lower()
    if extension not in {'csv', 'json'}:
        raise ValidationError('Selecione um arquivo .csv ou .json.')
    if upload.size > MAX_IMPORT_SIZE:
        raise ValidationError('O arquivo deve ter no máximo 5 MB.')
    raw = upload.read(MAX_IMPORT_SIZE + 1)
    if len(raw) > MAX_IMPORT_SIZE:
        raise ValidationError('O arquivo deve ter no máximo 5 MB.')
    try:
        text = raw.decode('utf-8-sig')
    except UnicodeDecodeError as exc:
        raise ValidationError('Salve o arquivo com codificação UTF-8.') from exc

    try:
        if extension == 'json':
            entries = json.loads(text)
            if not isinstance(entries, list):
                raise ValidationError('O JSON deve conter uma lista de palavras.')
        else:
            reader = csv.DictReader(io.StringIO(text, newline=''), strict=True)
            headers = reader.fieldnames
            if headers not in (['Palavra', 'Significado', 'Observação'], ['Palavra', 'Significado']):
                raise ValidationError('O CSV deve ter as colunas Palavra, Significado e, opcionalmente, Observação, nessa ordem.')
            entries = []
            for row in reader:
                if None in row or any(value is None for value in row.values()):
                    raise ValidationError(f'Linha {reader.line_num}: quantidade de colunas inválida.')
                entries.append({
                    'word': row['Palavra'],
                    'note': row.get('Observação', ''),
                    'meanings': [row['Significado']] if row['Significado'].strip() else [],
                })
    except (json.JSONDecodeError, csv.Error, RecursionError) as exc:
        raise ValidationError('Arquivo inválido. Confira a estrutura do CSV ou JSON.') from exc

    records = {}
    for index, entry in enumerate(entries, start=1):
        if not isinstance(entry, dict) or not isinstance(entry.get('meanings'), list):
            raise ValidationError(f'Registro {index}: informe word, note e uma lista meanings.')
        word, note, meanings = entry.get('word'), entry.get('note', ''), entry['meanings']
        values = [word, note, *meanings]
        if any(not isinstance(value, str) or '\x00' in value for value in values):
            raise ValidationError(f'Registro {index}: palavras, observações e significados devem ser textos válidos.')
        try:
            for value in values:
                value.encode('utf-8')
        except UnicodeEncodeError as exc:
            raise ValidationError(f'Registro {index}: o texto contém caracteres inválidos.') from exc
        word = word.strip().upper()
        note = note.upper()
        meanings = [meaning.upper() for meaning in meanings]
        if not word or len(word) > 120:
            raise ValidationError(f'Registro {index}: a palavra deve ter entre 1 e 120 caracteres.')
        key = word.casefold()
        record = records.setdefault(key, {'word': word, 'note': note, 'meanings': []})
        if record['note'] and note and record['note'] != note:
            raise ValidationError(f'Registro {index}: há observações diferentes para a mesma palavra.')
        if note:
            record['note'] = note
        existing = {meaning.casefold() for meaning in record['meanings']}
        for meaning in meanings:
            if not meaning.strip():
                raise ValidationError(f'Registro {index}: um significado não pode estar vazio.')
            if meaning.casefold() not in existing:
                record['meanings'].append(meaning)
                existing.add(meaning.casefold())
    if not records:
        raise ValidationError('O arquivo não contém palavras para importar.')
    return records


@transaction.atomic
def import_word_records(records, replace=False):
    stats = {'created_words': 0, 'created_meanings': 0, 'updated_words': 0}
    existing = {}
    for word in EnglishWord.objects.select_for_update().order_by('id'):
        key = word.word.strip().casefold()
        if key in existing and key in records:
            raise ValidationError('Há palavras duplicadas no cadastro. Corrija as duplicatas antes de importar.')
        existing[key] = word

    for key, entry in records.items():
        word = existing.get(key)
        updated = False
        if word is None:
            word = EnglishWord.objects.create(word=entry['word'], note=entry['note'])
            stats['created_words'] += 1
        else:
            fields = []
            if word.word != word.word.upper():
                word.word = word.word.upper()
                fields.append('word')
            if (replace or not word.note) and word.note != entry['note']:
                word.note = entry['note']
                fields.append('note')
            if word.note != word.note.upper():
                word.note = word.note.upper()
                if 'note' not in fields:
                    fields.append('note')
            if fields:
                word.save(update_fields=fields)
                updated = True
            for meaning in word.meanings.select_for_update().order_by('id'):
                if meaning.text != meaning.text.upper():
                    meaning.text = meaning.text.upper()
                    meaning.save(update_fields=['text'])
                    updated = True
            current = list(word.meanings.order_by('id').values_list('text', flat=True))
            if replace:
                if current != entry['meanings']:
                    word.meanings.all().delete()
                    updated = True
                else:
                    if updated:
                        stats['updated_words'] += 1
                    continue
        known = {meaning.casefold() for meaning in word.meanings.values_list('text', flat=True)}
        additions = [meaning for meaning in entry['meanings'] if meaning.casefold() not in known]
        EnglishMeaning.objects.bulk_create([EnglishMeaning(word=word, text=meaning) for meaning in additions])
        stats['created_meanings'] += len(additions)
        if key in existing and (updated or additions):
            stats['updated_words'] += 1
    return stats


def export_word_records():
    return [
        {'word': word.word, 'note': word.note, 'meanings': [meaning.text for meaning in word.meanings.all()]}
        for word in EnglishWord.objects.order_by('word', 'id').prefetch_related('meanings')
    ]
