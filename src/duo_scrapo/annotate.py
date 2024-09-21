from collections.abc import Sequence
from typing import Self
from attrs import define, field
from morfeusz2 import Morfeusz

@define
class Word:
    word: str = field()
    root: str = field()
    tags: list[str] = field()
    raw_tag: str = field()

class Morf:
    morfeusz = Morfeusz()

    def analyze(self: Self, lemma: str):
        result = self.morfeusz.analyse(lemma)
        return result

    def generate(self: Self, lemma: str, tag_id: str | None = None) -> Sequence[Word]:
        result = self.morfeusz.generate(lemma, tag_id)

        words: list[Word] = []
        for thing in result:
            tags = thing[2].split(":")
            words.append(
                Word(word=thing[0], tags=tags, root=thing[1], raw_tag=thing[2])
            )

        return words

m = Morf()
result = m.analyze("mówienie")
print(result)
