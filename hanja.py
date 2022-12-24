"""
Find the hanja characters that appear most often in the sino-korean words
in my Korean anki deck.
"""
from anki.collection import Collection
from anki.notes import Note
from collections import defaultdict

words_by_hanja_character = defaultdict(list)

COLLECTION_PATH = "/Users/mat/Library/Application Support/Anki2/User 1/collection.anki2"
KOREAN_DECK = '1541100429539'
COMMON_CJK_CHARACTERS = range(0x4E00, 0x9FFF)

col = Collection(COLLECTION_PATH)
note_ids = col.find_notes('deck:Korean AND "note:korean comprehension + production"')
for note_id in note_ids:
  note = Note(col=col, id=note_id)
  items = dict(note.items())
  hanja = items['Hanja'].strip()
  korean = items['Korean']
  english = items['English']

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
