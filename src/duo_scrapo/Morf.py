from typing import Literal, Self
from collections.abc import Iterable, Iterator, MutableSet, Set, Hashable

from morfeusz2 import Morfeusz
from attrs import define, field

from duo_scrapo.tag import Tag


@define
class VocabularyWord:
    word: str = field()
    definition: str = field()


@define(hash=True)
class Lemma:
    word: str = field()
    tags: str = field(kw_only=True)

    def to_str(self: Self) -> str:
        return ":".join(list(filter(None, [self.word, self.tags])))

    def __repr__(self) -> str:
        return f"'{self.to_str()}'"

    def matches(self: Self, other: Self | str) -> Literal[False] | int:
        o = other if isinstance(other, Lemma) else Lemma.from_str(other)

        if self.word != o.word:
            return False

        m = list(filter(lambda tag: tag in self.tags, o.tags))

        return len(m) + 1

    @classmethod
    def from_str(cls: type[Self], string: str):
        (word, tags) = string.split(":") if ":" in string else (string, "")
        return cls(word=word, tags=tags)


@define
class Word(Hashable):
    word: str = field()
    lemma: Lemma = field()
    tags: Set[Tag] = field(kw_only=True)
    # raw_tag: str = field(kw_only=True)
    data1: Set[str] = field(kw_only=True, default=set(), repr=False)
    data2: Set[str] = field(kw_only=True, default=set(), repr=False)

    def __hash__(self) -> int:
        return hash(f"{self.word}|{self.lemma.to_str()}|{self.tags}")


@define
class Analysis:
    word: str = field()


class WordList(MutableSet[Word]):
    sequence: list[int]
    container: dict[int, Word]

    def __init__(self) -> None:
        super().__init__()
        self.current = None
        self.sequence = []
        self.container = {}

    def __contains__(self, x: object) -> bool:
        return False

    def __iter__(self) -> Iterator[Word]:
        return list(self.container.values()).__iter__()

    def __len__(self) -> int:
        return self.container.__len__()

    def add(self, value: Word) -> None:
        h = hash(value)
        if h not in self.container:
            self.container[h] = value
        if h not in self.sequence:
            self.sequence.append(h)

    def discard(self, value: Word) -> None:
        h = hash(value)
        if h in self.container:
            self.container.pop(h)
            self.sequence.remove(h)


class Morf:
    dict_names: list[str] = field()
    morfeuszes: list[Morfeusz]

    def __init__(
            self,
            *,
            dict_names: Literal["sgjp", "polimorf"] | Iterable[Literal["sgjp", "polimorf"]] = "polimorf",
            analyse: bool = True,
            generate: bool = True,
            expand_dag: bool = True,
            expand_tags: bool = False,
            expand_dot: bool = False,
            expand_underscore: bool = False,
            aggl: str | None = None,
            praet: str | None = None,
            separate_numbering: bool = True,
            case_handling: Literal[100, 101, 102] = 100,
            whitespace: Literal[301, 302, 303] = 301
        ):

        self.morfeuszes = []
        self.dict_names = [dict_names] if isinstance(dict_names, str) else list(dict_names)
        _dict_path: str | None = "/usr/share/morfeusz2/dictionaries"

        for dict_name in self.dict_names:
            self.morfeuszes.append(Morfeusz(
                aggl=aggl,
                analyse=analyse,
                case_handling=case_handling,
                dict_name=dict_name,
                dict_path=_dict_path,
                expand_dag=expand_dag,
                expand_dot=expand_dot,
                expand_tags=expand_tags,
                expand_underscore=expand_underscore,
                generate=generate,
                praet=praet,
                separate_numbering=separate_numbering,
                whitespace=whitespace,
            ))

    def analyze(self: Self, string: str) -> Set[Word]:
        words = WordList()

        for m in self.morfeuszes:
            for datum in m.analyse(string):
                match datum:
                    case [_, _, (word, lemma, tag, data1, data2)] | [(word, lemma, tag, data1, data2)]:
                        w = Word(
                            word=word,
                            lemma=Lemma.from_str(lemma),
                            tags={
                                Tag(tt) for t in tag.split(":")
                                    for tt in t.split(".")
                            },
                            data1=set(data1),
                            data2=set(data2),
                        )

                        if w not in words:
                            words.add(w)

        return words

    def generate(self: Self, lemma: str, tag_id: str | None = None) -> Set[Word]:

        words = WordList()
        for m in self.morfeuszes:
            result = m.generate(lemma, tag_id)
            for thing in result:
                tags = [tt for t in thing[2].split(":") for tt in t.split(".")]
                w = Word(
                    word=thing[0],
                    tags={Tag(t) for t in tags},
                    lemma=Lemma.from_str(thing[1]),
                    # raw_tag=thing[2],
                )
                if w not in words:
                    words.add(w)
                    # words.append(w)

        return words
