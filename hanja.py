"""
Find the hanja characters that appear most often in the sino-korean words
in my Korean anki deck.
"""
from anki.collection import Collection
from anki.notes import Note
from collections import defaultdict
from data_cleaning import extract_word

from config import VocabFields, COLLECTION_PATH, VOCAB_NOTES, COMMON_CJK_CHARACTERS

words_by_hanja_character = defaultdict(list)

col = Collection(COLLECTION_PATH)
note_ids = col.find_notes(VOCAB_NOTES)
for note_id in note_ids:
  note = Note(col=col, id=note_id)
  items = dict(note.items())
  hanja = items[VocabFields.HANJA].strip()
  korean = extract_word(items[VocabFields.KOREAN])
  english = extract_word(items[VocabFields.ENGLISH])

  for character in hanja:
    if(ord(character)) not in COMMON_CJK_CHARACTERS:
      continue
    words_by_hanja_character[character].append((korean, english))

col.close()

sorted_characters = sorted(words_by_hanja_character.items(), key=lambda item: len(item[1]), reverse=True)
for character_item in sorted_characters[:10]:
  character, examples = character_item
  print(character)
  print(examples)
  print('')
