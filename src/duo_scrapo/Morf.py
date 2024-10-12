from functools import reduce
from typing import Literal, Self
from collections.abc import Iterable, Iterator, Set, Hashable

from morfeusz2 import Morfeusz
from attrs import define, field

from .tag import Tag
from .words.nouns import NounForms, CaseForms
from .words.verbs import VerbForms


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


def tags_from_str(string: str) -> Set[str]:
    return frozenset({t for tag in string.split(":") for t in tag.split(".")})


@define
class Word(Hashable):
    word: str = field()
    lemma: Lemma = field()
    tags: Set[str] = field(kw_only=True, converter=tags_from_str)
    # raw_tag: str = field(kw_only=True)
    data1: Set[str] = field(kw_only=True, default=set(), repr=False)
    data2: Set[str] = field(kw_only=True, default=set(), repr=False)

    def __hash__(self) -> int:
        return hash(f"{self.word}|{self.lemma.to_str()}|{self.tags}")

    def is_adj(self) -> bool:
        return bool(self.tags >= Tag.ADJECTIVE)

    def is_noun(self) -> bool:
        return bool(self.tags >= Tag.NOUN)

    def is_verb(self) -> bool:
        return bool(self.tags >= Tag.INFINITIVE)


@define
class Analysis:
    word: str = field()


class WordList(Set[Word]):
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


@define
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
                            tags=tag,
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
                w = Word(
                    word=thing[0],
                    tags=thing[2],
                    lemma=Lemma.from_str(thing[1]),
                    # raw_tag=thing[2],
                )
                if w not in words:
                    words.add(w)
                    # words.append(w)

        return words

    class NotANounError(Exception):
        """Raised when the word is not a noun"""

    def decline_noun(self, noun: str | Word):
        def reducer(acc: Word | None, cur: Word):
            if cur.lemma.to_str() == (noun if isinstance(noun, str) else noun.word):
                return cur
            return acc

        word = reduce(
            reducer,
            list(self.analyze(noun)),
            Word(word=noun, lemma=Lemma(word=noun, tags=""), tags="", data1=set(), data2=set())
        ) if isinstance(noun, str) else reducer(None, noun)

        if word is None or not word.is_noun():
            return None

        forms = NounForms(
            rodzaj=(Tag.Gender & word.tags),
            liczba_mnoga=CaseForms(
                mianownik="",
                dopełniacz="",
                celownik="",
                biernik="",
                miejscownik="",
                narzędnik="",
                wołacz="",
            ),
            liczba_pojedyncza=CaseForms(
                mianownik="",
                dopełniacz="",
                celownik="",
                biernik="",
                miejscownik="",
                narzędnik="",
                wołacz="",
            ),
        )

        s = word.lemma.to_str()
        generated = self.generate(s)
        for form in generated:
            number = Tag.Number & form.tags
            obj = forms.liczba_mnoga if number == Tag.PLURAL else forms.liczba_pojedyncza

            if form.tags >= Tag.NOMINATIVE:
                obj.mianownik = form.word
            if form.tags >= Tag.GENITIVE:
                obj.dopełniacz = form.word
            if form.tags >= Tag.DATIVE:
                obj.celownik = form.word
            if form.tags >= Tag.ACCUSATIVE:
                obj.biernik = form.word
            if form.tags >= Tag.LOCATIVE:
                obj.miejscownik = form.word
            if form.tags >= Tag.INSTRUMENTAL:
                obj.narzędnik = form.word
            if form.tags >= Tag.VOCATIVE:
                obj.wołacz = form.word

        return forms if (not forms.liczba_mnoga.is_empty() and not forms.liczba_pojedyncza.is_empty()) else None

    def conjugate_verb(self, verb: str | Word):
        def reducer(acc: Word | None, cur: Word):
            if cur.lemma.to_str() == (verb if isinstance(verb, str) else verb.word):
                return cur
            return acc

        word = reduce(
            reducer,
            list(self.analyze(verb)),
            Word(word=verb, lemma=Lemma(word=verb, tags=""), tags="", data1=set(), data2=set())
        ) if isinstance(verb, str) else reducer(None, verb)

        if word is None or not word.is_verb():
            return None

        aspekt = Tag.Aspect & word.tags

        forms = VerbForms(aspekt=aspekt)

        s = word.lemma.to_str()
        generated = self.generate(s)

        for form in generated:
            if form.tags >= Tag.INFINITIVE:
                forms.bezokolicznik = form.word
                continue

            if form.tags >= Tag.FINITIVE:
                if form.tags >= Tag.SINGULAR:
                    if form.tags >= Tag.FIRST:
                        forms._czas_teraźniejszy.liczba_pojedyncza.pierwsza_osoba = form.word  # type: ignore[assignment]
                    elif form.tags >= Tag.SECOND:
                        forms._czas_teraźniejszy.liczba_pojedyncza.druga_osoba = form.word  # type: ignore[assignment]
                    elif form.tags >= Tag.THIRD:
                        forms._czas_teraźniejszy.liczba_pojedyncza.trzecia_osoba = form.word  # type: ignore[assignment]
                elif form.tags >= Tag.PLURAL:
                    if form.tags >= Tag.FIRST:
                        forms._czas_teraźniejszy.liczba_mnoga.pierwsza_osoba = form.word  # type: ignore[assignment]
                    elif form.tags >= Tag.SECOND:
                        forms._czas_teraźniejszy.liczba_mnoga.druga_osoba = form.word  # type: ignore[assignment]
                    elif form.tags >= Tag.THIRD:
                        forms._czas_teraźniejszy.liczba_mnoga.trzecia_osoba = form.word  # type: ignore[assignment]

            elif form.tags >= Tag.PARTICIPLE_L:
                if form.tags >= Tag.SINGULAR:
                    for t in form.tags & Tag.Gender:
                        setattr(forms.rdzeń_czasu_przeszłego.liczba_pojedyncza, t, form.word)
                elif form.tags >= Tag.PLURAL:
                    if form.tags & Tag.MASCULINE_HUMAN:
                        forms.rdzeń_czasu_przeszłego.liczba_mnoga.m1 = form.word
                    else:
                        forms.rdzeń_czasu_przeszłego.liczba_mnoga.reszta = form.word

        return forms
