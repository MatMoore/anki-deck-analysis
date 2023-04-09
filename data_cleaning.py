"""
My notes contain formatting and parenthetical text
(e.g. distinguishing between homonyms or categorizing the word)

This module provides functions to strip all that out.

Note: This does not currently strip out hanja hints included in the Korean field.
"""
import re

# https://github.com/pallets/markupsafe/blob/0.23/markupsafe/__init__.py#L21
HTML_TAG_REGEX = re.compile(r'\s*(<!--.*?-->|<[^>]*>|&nbsp;|\[[^\]]*\])\s*')
PAREN_REGEX = re.compile(r'\([^)]+\)')


def strip_html(text):
  '''
  Return text with html tags, entities, and anki markup stripped out
  '''
  return HTML_TAG_REGEX.sub(' ', text).strip()


def strip_parens(text):
  '''
  Remove text in parentheses from a string
  e.g.
  foo (bar) -> foo
  '''
  return PAREN_REGEX.sub('', text).strip()


def extract_word(text):
  '''
  Remove html tags, entities, anki markup and parenthetical text.
  '''
  return strip_parens(strip_html(text))
