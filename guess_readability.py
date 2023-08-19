import sys
from pathlib import Path
from dictionary import load_vocab
from konlpy.tag import Kkma

analyzer = Kkma()

dictionary = load_vocab()

known_nouns = set()
for term in dictionary:
    known_nouns.update(analyzer.nouns(term.value))


def percent_known_nouns(text):
    """
    Percentage of nouns that appear in the dictionary
    """
    known_count = 0
    nouns = analyzer.nouns(text)
    for noun in nouns:
        if noun in known_nouns:
            known_count += 1

    return known_count / len(nouns)


if __name__ == '__main__':
    path = Path(sys.argv[1])
    results = []
    for filename in path.glob("*.txt"):
        with filename.open() as f:
            text = f.read()
            metric = percent_known_nouns(text)
            results.append((metric, filename))

    print(min(results))
    print(max(results))

    for metric, filename in sorted(results, reverse=True)[:10]:
        print(f"{metric} {filename}")
