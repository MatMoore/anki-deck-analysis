import pytest
from data_cleaning import strip_html, strip_parens, extract_word

@pytest.mark.parametrize(
  "raw,expected",
  [
    ('hello <b>world</b>', 'hello world'),
    ('thing <img src="abc">', 'thing'),
    ('hello<br>world', 'hello world'),
    ('hello<br/>world', 'hello world'),
    ('hello<div>world</div>', 'hello world')
  ]
)
def test_strip_html(raw, expected):
    assert strip_html(raw) == expected


@pytest.mark.parametrize(
  "raw,expected",
  [
    ('hello (world)', 'hello'),
    ('(hello) world', 'world'),
  ]
)
def test_strip_parens(raw, expected):
    assert strip_parens(raw) == expected


@pytest.mark.parametrize(
  "raw,expected",
  [
    ('<b>hello<b/> (world)', 'hello'),
    ('(hello)\n\nworld', 'world'),
  ]
)
def test_extract_word(raw, expected):
    assert extract_word(raw) == expected
