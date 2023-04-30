"""
Load different kinds of notes into memory from the collection
to form dictionaries and corpuses.
"""

from anki.collection import Collection
from anki.notes import Note

from config import VocabFields, COLLECTION_PATH, VOCAB_NOTES, HANJA_NOTES, HanjaFields
from data_cleaning import extract_word, extract_hanjas

from typing import NamedTuple

class Term(NamedTuple):
  value: str
  meaning: str
  extra: dict


class Dictionary:
  def __init__(self):
    self._terms = {}

  def add(self, value, meaning, extra=None):
    self._terms[value] = Term(value, meaning, dict(extra or {}))

  def lookup(self, value):
    return self._terms.get(value)

  def __iter__(self):
    return iter(self._terms.values())


def load_vocab():
  dictionary = Dictionary()
  col = Collection(COLLECTION_PATH)
  note_ids = col.find_notes(VOCAB_NOTES)
  notes = [Note(col=col, id=note_id) for note_id in note_ids]

  for note in notes:
    items = dict(note.items())
    korean = extract_word(items[VocabFields.KOREAN])
    meaning = extract_word(items[VocabFields.ENGLISH])
    hanja = extract_hanjas(items[VocabFields.HANJA])

    dictionary.add(korean, meaning, extra={'hanja': hanja})

  col.close()

  return dictionary


def load_hanja():
  dictionary = Dictionary()
  col = Collection(COLLECTION_PATH)
  note_ids = col.find_notes(HANJA_NOTES)
  notes = [Note(col=col, id=note_id) for note_id in note_ids]

  for note in notes:
    items = dict(note.items())
    hanja = items[HanjaFields.HANJA].strip()
    meaning = items[HanjaFields.MEANING].strip()

    dictionary.add(hanja, meaning)

  col.close()

  return dictionary
