"""
Suggest new words based on example sentences
"""
from anki.collection import Collection
from anki.notes import Note
import spacy
import re
from koparadigm import Paradigm

nlp = spacy.load("ko_core_news_md")
conjugator = Paradigm()

COLLECTION_PATH = "/Users/mat/Library/Application Support/Anki2/User 1/collection.anki2"
KOREAN_DECK = '1541100429539'
KOREAN_WORD_REGEX = re.compile(r'[\uAC00-\uD7AF]+')

HTML_TAG_REGEX = re.compile(r'(<!--.*?-->|<[^>]*>|&nbsp;|\[[^\]]*\])') # https://github.com/pallets/markupsafe/blob/0.23/markupsafe/__init__.py#L21

col = Collection(COLLECTION_PATH)
note_ids = col.find_notes('deck:Korean AND "note:korean comprehension + production"')

words = set()
docs = []


def verb_stem(word):
  '''
  Given a dictionary form like 먹다, return the stem 먹
  '''
  if word.endswith('다') and len(word) > 1:
    return word[:-1]

  return word


def looks_verby(word):
  '''
  Check whether a word looks like it could be a verb in dictionary form,
  i.e. it ends with 다. This may have some false positives.
  '''
  return word.endswith('다')


def index_word(word):
  '''
  Add a word to the list of known words.
  If it looks like a verb, include various conjugations as well.
  Otherwise, include various particles.

  This allows us to use morphological comparisons later on when checking
  whether a word in a sentence is known or not.

  TODO: decide how to handle particles appended to noun forms
  '''
  words.add(word)

  if looks_verby(word):
    stem = verb_stem(word)
    verbs = conjugator.conjugate(stem)
    if verbs is None:
      return
    for verb in verbs:
      for _inflection, variations in verb[1]:
        for variation in variations.split('/'):
          words.add(variation)
  else:
    for particle in ('이', '가', '에', '로', '으로', '은', '는', '를', '을', '에서', '게서', '게', '게서는', '한테', '에게', '님'):
      words.add(word + particle)


def process_sentence(sentence):
  '''
  Run an example sentence through the Spacy pipeline
  '''
  if not sentence:
    return

  docs.append(nlp(sentence))


def ignore_pos(pos):
  '''
  Decide whether to ignore a token based on the part-of-speech tag
  '''
  return pos not in 'VERB'

  #return pos in (
  #  'PUNCT',
  #  'ADV',
  #  'PRON',
  #  'PROPN',
  #  'AUX',
  #  'DET'
  #)

def is_korean_word(text):
  '''
  Whether a word is made up of Hangeul characters
  '''
  return KOREAN_WORD_REGEX.match(text)


def strip_html(text):
  '''
  Return text with html tags, entities, anki markup stripped out
  '''
  return HTML_TAG_REGEX.sub(' ', text)


for word in [
  '있다',
  '없다',
  '이다',
  '나다',
  '그렇다',
  '이렇다',
  '어떻다',
  '하다',
  '가다',
  '오다',
  '알다',
  '모르다',
  '먹다',
  '마시다',
  '많다',
  '같다',
  '괜찮다',
]:
  index_word(word)

for note_id in note_ids:
  note = Note(col=col, id=note_id)
  items = dict(note.items())
  example1 = items['Korean example sentence 1']
  example2 = items['Korean example sentence 2']
  korean = items['Korean']

  korean = strip_html(korean)
  example1 = strip_html(example1)
  example2 = strip_html(example2)

  for word in korean.strip().split(' '):
    index_word(word)
  process_sentence(example1)
  process_sentence(example2)


for doc in docs:
  for token in doc:
    if ignore_pos(token.pos_):
      continue
    if not is_korean_word(token.text):
      continue
    #print(token.pos_)
    #print(token.text)

    if token.text not in words:
      print(f'New word: {token.text} ({token.pos_})')
