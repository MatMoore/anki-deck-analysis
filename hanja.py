"""
Find the hanja characters that appear most often in the sino-korean words
in my Korean anki deck.
"""
from collections import defaultdict
from dictionary import load_hanja, load_vocab


def format_example(note, hanja):
  return f'{hanja}: {note.value} ({note.meaning})'


studied_hanja = load_hanja()
notes = load_vocab()

words_by_hanja_character = defaultdict(list)

for note in notes:
  for hanja in note.extra['hanja']:
    for hanja_character in hanja:
      if studied_hanja.lookup(hanja_character):
        continue
      words_by_hanja_character[hanja_character].append(
        format_example(note, hanja)
      )


sorted_characters = sorted(words_by_hanja_character.items(), key=lambda item: len(item[1]), reverse=True)
for character_item in sorted_characters[:10]:
  character, examples = character_item
  print(character)
  print('\n'.join(examples))
  print('')
