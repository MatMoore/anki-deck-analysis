"""
Pick some random words that I don't know well,
so that I can practice using them in sentences
"""

from anki.collection import Collection
from anki.notes import Note
from random import sample

from config import VocabFields, COLLECTION_PATH, VOCAB_NOTES, COMMON_CJK_CHARACTERS


col = Collection(COLLECTION_PATH)
note_ids = col.find_notes(VOCAB_NOTES + ' AND tag:leech')
notes = [Note(col=col, id=note_id) for note_id in note_ids]
chosen = sample(notes, 3)

for note in chosen:
  items = dict(note.items())
  hanja = items[VocabFields.HANJA].strip()
  korean = items[VocabFields.KOREAN]
  english = items[VocabFields.ENGLISH]

  print(f"{korean} - {english}")

col.close()
