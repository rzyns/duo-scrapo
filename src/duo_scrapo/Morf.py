from functools import reduce
from typing import Literal, NamedTuple, Self, TypeGuard
from collections.abc import Callable, Iterable, Iterator, Set, Hashable

import attr
import attrs
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
class _CaseForms:
    mianownik: str
    dopełniacz: str
    celownik: str
    biernik: str
    miejscownik: str
    narzędnik: str
    wołacz: str

    def is_empty(self) -> bool:
        return not any(attr.asdict(self).values())


@define
class NounForms:
    rodzaj: Tag
    liczba_pojedyncza: _CaseForms
    liczba_mnoga: _CaseForms

    def __repr__(self) -> str:
        lines = [
            f"rodzaj: {self.rodzaj}",
            "liczba pojedyncza:",
            f"    mianownik:   {self.liczba_pojedyncza.mianownik}",
            f"    dopełniacz:  {self.liczba_pojedyncza.dopełniacz}",
            f"    celownik:    {self.liczba_pojedyncza.celownik}",
            f"    biernik:     {self.liczba_pojedyncza.biernik}",
            f"    miejscownik: {self.liczba_pojedyncza.miejscownik}",
            f"    narzędnik:   {self.liczba_pojedyncza.narzędnik}",
            f"    wołacz:      {self.liczba_pojedyncza.wołacz}",
            "liczba mnoga:",
            f"    mianownik:   {self.liczba_mnoga.mianownik}",
            f"    dopełniacz:  {self.liczba_mnoga.dopełniacz}",
            f"    celownik:    {self.liczba_mnoga.celownik}",
            f"    biernik:     {self.liczba_mnoga.biernik}",
            f"    miejscownik: {self.liczba_mnoga.miejscownik}",
            f"    narzędnik:   {self.liczba_mnoga.narzędnik}",
            f"    wołacz:      {self.liczba_mnoga.wołacz}",
        ]

        return "\n".join(lines)


@define
class _VerbPersonForms[T]:
    pierwsza_osoba: T
    druga_osoba: T
    trzecia_osoba: T

    @classmethod
    def empty(cls, empty: T | Callable[[], T]) -> Self:
        return cls(
            pierwsza_osoba=empty if not callable(empty) else empty(),
            druga_osoba=empty if not callable(empty) else empty(),
            trzecia_osoba=empty if not callable(empty) else empty(),
        )

    def is_empty(self) -> bool:
        return not any(attr.asdict(self).values())


@define
class Numbered[T, U]:
    liczba_pojedyncza: T
    liczba_mnoga: U

    @classmethod
    def empty(cls, empty_lp: T | Callable[[], T], empty_lm: U | Callable[[], U]) -> Self:
        return cls(
            liczba_pojedyncza=empty_lp if not callable(empty_lp) else empty_lp(),
            liczba_mnoga=empty_lm if not callable(empty_lm) else empty_lm(),
        )


@define
class GenderedSingular[T]:
    m1: T = attrs.field()
    m2: T = attrs.field()
    m3: T = attrs.field()
    f:  T = attrs.field()
    n:  T = attrs.field()

    @classmethod
    def empty(cls, empty: T | Callable[[], T]) -> Self:
        return cls(
            m1=empty if not callable(empty) else empty(),
            m2=empty if not callable(empty) else empty(),
            m3=empty if not callable(empty) else empty(),
            f=empty if not callable(empty) else empty(),
            n=empty if not callable(empty) else empty(),
        )


@define
class GenderedPlural[T]:
    m1: T = attrs.field(default=None)
    reszta: T = attrs.field(default=None)

    @classmethod
    def empty(cls, empty: T | Callable[[], T]) -> Self:
        return cls(
            m1=empty if not callable(empty) else empty(),
            reszta=empty if not callable(empty) else empty(),
        )


@define
class Gendered[T]:
    liczba_pojedyncza: GenderedSingular[T] = attrs.field()
    liczba_mnoga: GenderedPlural[T] = attrs.field()

    @classmethod
    def empty(cls, empty: T | Callable[[], T]) -> Self:
        return cls(
            liczba_pojedyncza=GenderedSingular[T].empty(empty),
            liczba_mnoga=GenderedPlural[T].empty(empty),
        )


type VERB_CSV_ROW = tuple[
    str,  # "aspekt",

    str,  # "bezokolicznik",
    # "bezosobnik",
    # "imiesłów_przymiotnikowy",

    str,  # teraz    sg 1p
    str,  # teraz    sg 2p
    str,  # teraz    sg 3p
    str,  # teraz    pl 1p
    str,  # teraz    pl 2p
    str,  # teraz    pl 3p

    str,  # przeszły sg 1p m1
    str,  # przeszły sg 1p m2
    str,  # przeszły sg 1p m3
    str,  # przeszły sg 1p f
    str,  # przeszły sg 1p n
    str,  # przeszły sg 2p m1
    str,  # przeszły sg 2p m2
    str,  # przeszły sg 2p m3
    str,  # przeszły sg 2p f
    str,  # przeszły sg 2p n
    str,  # przeszły sg 3p m1
    str,  # przeszły sg 3p m2
    str,  # przeszły sg 3p m3
    str,  # przeszły sg 3p f
    str,  # przeszły sg 3p n
    str,  # przeszły pl 1p m1
    str,  # przeszły pl 1p r
    str,  # przeszły pl 2p m1
    str,  # przeszły pl 2p r
    str,  # przeszły pl 3p m1
    str,  # przeszły pl 3p r

    str,  # przyszły sg 1p m1
    str,  # przyszły sg 1p m2
    str,  # przyszły sg 1p m3
    str,  # przyszły sg 1p f
    str,  # przyszły sg 1p n
    str,  # przyszły sg 2p m1
    str,  # przyszły sg 2p m2
    str,  # przyszły sg 2p m3
    str,  # przyszły sg 2p f
    str,  # przyszły sg 2p n
    str,  # przyszły sg 3p m1
    str,  # przyszły sg 3p m2
    str,  # przyszły sg 3p m3
    str,  # przyszły sg 3p f
    str,  # przyszły sg 3p n
    str,  # przyszły pl 1p m1
    str,  # przyszły pl 1p r
    str,  # przyszły pl 2p m1
    str,  # przyszły pl 2p r
    str,  # przyszły pl 3p m1
    str,  # przyszły pl 3p r
]


class CsvRow(NamedTuple):
    aspekt: str

    bezokolicznik: str

    teraz_sg_1p: str
    teraz_sg_2p: str
    teraz_sg_3p: str
    teraz_pl_1p: str
    teraz_pl_2p: str
    teraz_pl_3p: str

    przeszły_sg_1p_m1: str
    przeszły_sg_1p_m2: str
    przeszły_sg_1p_m3: str
    przeszły_sg_1p_f: str
    przeszły_sg_1p_n: str
    przeszły_sg_2p_m1: str
    przeszły_sg_2p_m2: str
    przeszły_sg_2p_m3: str
    przeszły_sg_2p_f: str
    przeszły_sg_2p_n: str
    przeszły_sg_3p_m1: str
    przeszły_sg_3p_m2: str
    przeszły_sg_3p_m3: str
    przeszły_sg_3p_f: str
    przeszły_sg_3p_n: str
    przeszły_pl_1p_m1: str
    przeszły_pl_1p_r: str
    przeszły_pl_2p_m1: str
    przeszły_pl_2p_r: str
    przeszły_pl_3p_m1: str
    przeszły_pl_3p_r: str

    przyszły_sg_1p_m1: str
    przyszły_sg_1p_m2: str
    przyszły_sg_1p_m3: str
    przyszły_sg_1p_f: str
    przyszły_sg_1p_n: str
    przyszły_sg_2p_m1: str
    przyszły_sg_2p_m2: str
    przyszły_sg_2p_m3: str
    przyszły_sg_2p_f: str
    przyszły_sg_2p_n: str
    przyszły_sg_3p_m1: str
    przyszły_sg_3p_m2: str
    przyszły_sg_3p_m3: str
    przyszły_sg_3p_f: str
    przyszły_sg_3p_n: str
    przyszły_pl_1p_m1: str
    przyszły_pl_1p_r: str
    przyszły_pl_2p_m1: str
    przyszły_pl_2p_r: str
    przyszły_pl_3p_m1: str
    przyszły_pl_3p_r: str


@define
class VerbForms:
    aspekt: Tag
    bezokolicznik: str = attrs.field(default="")

    # Present tense _form_
    _czas_teraźniejszy: Numbered[_VerbPersonForms[str], _VerbPersonForms[str]] = attrs.field(
        default=Numbered[_VerbPersonForms[str], _VerbPersonForms[str]].empty(
            _VerbPersonForms[str].empty(""),
            _VerbPersonForms[str].empty(""),
        )
    )

    @property
    def czas_teraźniejszy(self) -> Numbered[_VerbPersonForms[str], _VerbPersonForms[str]]:
        if self.aspekt == Tag.PERFECTIVE:
            return Numbered[_VerbPersonForms[str], _VerbPersonForms[str]].empty(
                empty_lp=_VerbPersonForms[str].empty(""),
                empty_lm=_VerbPersonForms[str].empty(""),
            )
        return self._czas_teraźniejszy

    bezosobnik: str = attrs.field(default="")

    rdzeń_czasu_przeszłego: Gendered[str] = attrs.field(default=Gendered[str].empty(""))

    # mówił  = praet:sg:m1.m2.m3:imperf
    # mówiła = praet:sg:f:imperf
    # mówiło = praet:sg:n:imperf
    # mówili = praet:pl:m1:imperf
    # mówiły = praet:pl:m2.m3.f.n:imperf

    @property
    def czas_przeszły(self) -> Numbered[_VerbPersonForms[GenderedSingular[str]], _VerbPersonForms[GenderedPlural[str]]]:
        return Numbered(
            liczba_pojedyncza=_VerbPersonForms(
                pierwsza_osoba=GenderedSingular[str](
                    m1=f"{self.rdzeń_czasu_przeszłego.liczba_pojedyncza.m1}em",
                    m2=f"{self.rdzeń_czasu_przeszłego.liczba_pojedyncza.m2}em",
                    m3=f"{self.rdzeń_czasu_przeszłego.liczba_pojedyncza.m3}em",
                    f=f"{self.rdzeń_czasu_przeszłego.liczba_pojedyncza.f}m",
                    n=f"{self.rdzeń_czasu_przeszłego.liczba_pojedyncza.n}m"
                ),
                druga_osoba=GenderedSingular[str](
                    m1=f"{self.rdzeń_czasu_przeszłego.liczba_pojedyncza.m1}eś",
                    m2=f"{self.rdzeń_czasu_przeszłego.liczba_pojedyncza.m2}eś",
                    m3=f"{self.rdzeń_czasu_przeszłego.liczba_pojedyncza.m3}eś",
                    f=f"{self.rdzeń_czasu_przeszłego.liczba_pojedyncza.f}ś",
                    n=f"{self.rdzeń_czasu_przeszłego.liczba_pojedyncza.n}ś"
                ),
                trzecia_osoba=GenderedSingular[str](
                    m1=self.rdzeń_czasu_przeszłego.liczba_pojedyncza.m1,
                    m2=self.rdzeń_czasu_przeszłego.liczba_pojedyncza.m2,
                    m3=self.rdzeń_czasu_przeszłego.liczba_pojedyncza.m3,
                    f=self.rdzeń_czasu_przeszłego.liczba_pojedyncza.f,
                    n=self.rdzeń_czasu_przeszłego.liczba_pojedyncza.n
                ),
            ),
            liczba_mnoga=_VerbPersonForms(
                pierwsza_osoba=GenderedPlural[str](
                    m1=f"{self.rdzeń_czasu_przeszłego.liczba_mnoga.m1}śmy",
                    reszta=f"{self.rdzeń_czasu_przeszłego.liczba_mnoga.reszta}śmy",
                ),
                druga_osoba=GenderedPlural[str](
                    m1=f"{self.rdzeń_czasu_przeszłego.liczba_mnoga.m1}ście",
                    reszta=f"{self.rdzeń_czasu_przeszłego.liczba_mnoga.reszta}ście",
                ),
                trzecia_osoba=GenderedPlural[str](
                    m1=self.rdzeń_czasu_przeszłego.liczba_mnoga.m1,
                    reszta=self.rdzeń_czasu_przeszłego.liczba_mnoga.reszta,
                ),
            ),
        )

    # def czas_przeszły(self) -> Numbered[_VerbPersonForms[GenderedSingular[str]], _VerbPersonForms[GenderedPlural[str]]]:
    @property
    def czas_przyszły(self) -> Numbered[_VerbPersonForms[str], _VerbPersonForms[str]] | Numbered[_VerbPersonForms[GenderedSingular[str]], _VerbPersonForms[GenderedPlural[str]]]:
        if self.aspekt == Tag.IMPERFECTIVE:
            return self._czas_teraźniejszy

        return Numbered(
            liczba_pojedyncza=_VerbPersonForms(
                pierwsza_osoba=GenderedSingular[str](
                    m1=f"{self.rdzeń_czasu_przeszłego.liczba_pojedyncza.m1}em",
                    m2=f"{self.rdzeń_czasu_przeszłego.liczba_pojedyncza.m2}em",
                    m3=f"{self.rdzeń_czasu_przeszłego.liczba_pojedyncza.m3}em",
                    f=f"{self.rdzeń_czasu_przeszłego.liczba_pojedyncza.f}m",
                    n=f"{self.rdzeń_czasu_przeszłego.liczba_pojedyncza.n}m"
                ),
                druga_osoba=GenderedSingular[str](
                    m1=f"{self.rdzeń_czasu_przeszłego.liczba_pojedyncza.m1}eś",
                    m2=f"{self.rdzeń_czasu_przeszłego.liczba_pojedyncza.m2}eś",
                    m3=f"{self.rdzeń_czasu_przeszłego.liczba_pojedyncza.m3}eś",
                    f=f"{self.rdzeń_czasu_przeszłego.liczba_pojedyncza.f}ś",
                    n=f"{self.rdzeń_czasu_przeszłego.liczba_pojedyncza.n}ś"
                ),
                trzecia_osoba=GenderedSingular[str](
                    m1=self.rdzeń_czasu_przeszłego.liczba_pojedyncza.m1,
                    m2=self.rdzeń_czasu_przeszłego.liczba_pojedyncza.m2,
                    m3=self.rdzeń_czasu_przeszłego.liczba_pojedyncza.m3,
                    f=self.rdzeń_czasu_przeszłego.liczba_pojedyncza.f,
                    n=self.rdzeń_czasu_przeszłego.liczba_pojedyncza.n
                ),
            ),
            liczba_mnoga=_VerbPersonForms(
                pierwsza_osoba=GenderedPlural[str](
                    m1=f"{self.rdzeń_czasu_przeszłego.liczba_mnoga.m1}śmy",
                    reszta=f"{self.rdzeń_czasu_przeszłego.liczba_mnoga.reszta}śmy",
                ),
                druga_osoba=GenderedPlural[str](
                    m1=f"{self.rdzeń_czasu_przeszłego.liczba_mnoga.m1}ście",
                    reszta=f"{self.rdzeń_czasu_przeszłego.liczba_mnoga.reszta}ście",
                ),
                trzecia_osoba=GenderedPlural[str](
                    m1=self.rdzeń_czasu_przeszłego.liczba_mnoga.m1,
                    reszta=self.rdzeń_czasu_przeszłego.liczba_mnoga.reszta,
                ),
            ),
        )

    @classmethod
    def _is_teraz(cls, forms: Numbered[_VerbPersonForms[str], _VerbPersonForms[str]] | Numbered[_VerbPersonForms[GenderedSingular[str]], _VerbPersonForms[GenderedPlural[str]]]) -> TypeGuard[Numbered[_VerbPersonForms[str], _VerbPersonForms[str]]]:
        return isinstance(forms.liczba_mnoga.pierwsza_osoba, str)

    @classmethod
    def _is_gendered(cls, forms: Numbered[_VerbPersonForms[str], _VerbPersonForms[str]] | Numbered[_VerbPersonForms[GenderedSingular[str]], _VerbPersonForms[GenderedPlural[str]]]) -> TypeGuard[Numbered[_VerbPersonForms[GenderedSingular[str]], _VerbPersonForms[GenderedPlural[str]]]]:
        return isinstance(forms.liczba_mnoga.pierwsza_osoba, GenderedPlural)

    @staticmethod
    def get_cols() -> CsvRow:
        return CsvRow(
            "aspekt",
            "bezokolicznik",

            "teraz_sg_1p",
            "teraz_sg_2p",
            "teraz_sg_3p",
            "teraz_pl_1p",
            "teraz_pl_2p",
            "teraz_pl_3p",

            "przeszły_sg_1p_m1",
            "przeszły_sg_1p_m2",
            "przeszły_sg_1p_m3",
            "przeszły_sg_1p_f",
            "przeszły_sg_1p_n",
            "przeszły_sg_2p_m1",
            "przeszły_sg_2p_m2",
            "przeszły_sg_2p_m3",
            "przeszły_sg_2p_f",
            "przeszły_sg_2p_n",
            "przeszły_sg_3p_m1",
            "przeszły_sg_3p_m2",
            "przeszły_sg_3p_m3",
            "przeszły_sg_3p_f",
            "przeszły_sg_3p_n",
            "przeszły_pl_1p_m1",
            "przeszły_pl_1p_r",
            "przeszły_pl_2p_m1",
            "przeszły_pl_2p_r",
            "przeszły_pl_3p_m1",
            "przeszły_pl_3p_r",

            "przyszły_sg_1p_m1",
            "przyszły_sg_1p_m2",
            "przyszły_sg_1p_m3",
            "przyszły_sg_1p_f",
            "przyszły_sg_1p_n",
            "przyszły_sg_2p_m1",
            "przyszły_sg_2p_m2",
            "przyszły_sg_2p_m3",
            "przyszły_sg_2p_f",
            "przyszły_sg_2p_n",
            "przyszły_sg_3p_m1",
            "przyszły_sg_3p_m2",
            "przyszły_sg_3p_m3",
            "przyszły_sg_3p_f",
            "przyszły_sg_3p_n",
            "przyszły_pl_1p_m1",
            "przyszły_pl_1p_r",
            "przyszły_pl_2p_m1",
            "przyszły_pl_2p_r",
            "przyszły_pl_3p_m1",
            "przyszły_pl_3p_r",
        )

    def to_rows(self) -> CsvRow:
        if self._is_gendered(self.czas_przyszły):
            return CsvRow(
                str(self.aspekt),
                self.bezokolicznik,

                 self.czas_teraźniejszy.liczba_pojedyncza.pierwsza_osoba,  # teraz    sg 1p
                 self.czas_teraźniejszy.liczba_pojedyncza.druga_osoba,     # teraz    sg 2p
                 self.czas_teraźniejszy.liczba_pojedyncza.trzecia_osoba,   # teraz    sg 3p
                 self.czas_teraźniejszy.liczba_mnoga.pierwsza_osoba,       # teraz    pl 1p
                 self.czas_teraźniejszy.liczba_mnoga.druga_osoba,          # teraz    pl 2p
                 self.czas_teraźniejszy.liczba_mnoga.trzecia_osoba,        # teraz    pl 3p

                 self.czas_przeszły.liczba_pojedyncza.pierwsza_osoba.m1,   # przeszły sg 1p m1
                 self.czas_przeszły.liczba_pojedyncza.pierwsza_osoba.m2,   # przeszły sg 1p m2
                 self.czas_przeszły.liczba_pojedyncza.pierwsza_osoba.m3,   # przeszły sg 1p m3
                 self.czas_przeszły.liczba_pojedyncza.pierwsza_osoba.f,    # przeszły sg 1p f
                 self.czas_przeszły.liczba_pojedyncza.pierwsza_osoba.n,    # przeszły sg 1p n
                 self.czas_przeszły.liczba_pojedyncza.druga_osoba.m1,      # przeszły sg 2p m1
                 self.czas_przeszły.liczba_pojedyncza.druga_osoba.m2,      # przeszły sg 2p m2
                 self.czas_przeszły.liczba_pojedyncza.druga_osoba.m3,      # przeszły sg 2p m3
                 self.czas_przeszły.liczba_pojedyncza.druga_osoba.f,       # przeszły sg 2p f
                 self.czas_przeszły.liczba_pojedyncza.druga_osoba.n,       # przeszły sg 2p n
                 self.czas_przeszły.liczba_pojedyncza.trzecia_osoba.m1,    # przeszły sg 3p m1
                 self.czas_przeszły.liczba_pojedyncza.trzecia_osoba.m2,    # przeszły sg 3p m2
                 self.czas_przeszły.liczba_pojedyncza.trzecia_osoba.m3,    # przeszły sg 3p m3
                 self.czas_przeszły.liczba_pojedyncza.trzecia_osoba.f,     # przeszły sg 3p f
                 self.czas_przeszły.liczba_pojedyncza.trzecia_osoba.n,     # przeszły sg 3p n
                 self.czas_przeszły.liczba_mnoga.pierwsza_osoba.m1,        # przeszły pl 1p m1
                 self.czas_przeszły.liczba_mnoga.pierwsza_osoba.reszta,    # przeszły pl 1p r
                 self.czas_przeszły.liczba_mnoga.druga_osoba.m1,           # przeszły pl 2p m1
                 self.czas_przeszły.liczba_mnoga.druga_osoba.reszta,       # przeszły pl 2p r
                 self.czas_przeszły.liczba_mnoga.trzecia_osoba.m1,         # przeszły pl 3p m1
                 self.czas_przeszły.liczba_mnoga.trzecia_osoba.reszta,     # przeszły pl 3p r

                 self.czas_przyszły.liczba_pojedyncza.pierwsza_osoba.m1,   # przyszły sg 1p m1
                 self.czas_przyszły.liczba_pojedyncza.pierwsza_osoba.m2,   # przyszły sg 1p m2
                 self.czas_przyszły.liczba_pojedyncza.pierwsza_osoba.m3,   # przyszły sg 1p m3
                 self.czas_przyszły.liczba_pojedyncza.pierwsza_osoba.f,    # przyszły sg 1p f
                 self.czas_przyszły.liczba_pojedyncza.pierwsza_osoba.n,    # przyszły sg 1p n
                 self.czas_przyszły.liczba_pojedyncza.druga_osoba.m1,      # przyszły sg 2p m1
                 self.czas_przyszły.liczba_pojedyncza.druga_osoba.m2,      # przyszły sg 2p m2
                 self.czas_przyszły.liczba_pojedyncza.druga_osoba.m3,      # przyszły sg 2p m3
                 self.czas_przyszły.liczba_pojedyncza.druga_osoba.f,       # przyszły sg 2p f
                 self.czas_przyszły.liczba_pojedyncza.druga_osoba.n,       # przyszły sg 2p n
                 self.czas_przyszły.liczba_pojedyncza.trzecia_osoba.m1,    # przyszły sg 3p m1
                 self.czas_przyszły.liczba_pojedyncza.trzecia_osoba.m2,    # przyszły sg 3p m2
                 self.czas_przyszły.liczba_pojedyncza.trzecia_osoba.m3,    # przyszły sg 3p m3
                 self.czas_przyszły.liczba_pojedyncza.trzecia_osoba.f,     # przyszły sg 3p f
                 self.czas_przyszły.liczba_pojedyncza.trzecia_osoba.n,     # przyszły sg 3p n
                 self.czas_przyszły.liczba_mnoga.pierwsza_osoba.m1,        # przyszły pl 1p m1
                 self.czas_przyszły.liczba_mnoga.pierwsza_osoba.reszta,    # przyszły pl 1p r
                 self.czas_przyszły.liczba_mnoga.druga_osoba.m1,           # przyszły pl 2p m1
                 self.czas_przyszły.liczba_mnoga.druga_osoba.reszta,       # przyszły pl 2p r
                 self.czas_przyszły.liczba_mnoga.trzecia_osoba.m1,         # przyszły pl 3p m1
                 self.czas_przyszły.liczba_mnoga.trzecia_osoba.reszta,     # przyszły pl 3p r
             )
        elif self._is_teraz(self.czas_przyszły):
            return CsvRow(
                str(self.aspekt),
                self.bezokolicznik,
                self.czas_teraźniejszy.liczba_pojedyncza.pierwsza_osoba,
                self.czas_teraźniejszy.liczba_pojedyncza.druga_osoba,
                self.czas_teraźniejszy.liczba_pojedyncza.trzecia_osoba,
                self.czas_teraźniejszy.liczba_mnoga.pierwsza_osoba,
                self.czas_teraźniejszy.liczba_mnoga.druga_osoba,
                self.czas_teraźniejszy.liczba_mnoga.trzecia_osoba,

                self.czas_przeszły.liczba_pojedyncza.pierwsza_osoba.m1,  # przeszły 1p m1 sg
                self.czas_przeszły.liczba_pojedyncza.pierwsza_osoba.m2,  # przeszły 1p m2 sg
                self.czas_przeszły.liczba_pojedyncza.pierwsza_osoba.m3,  # przeszły 1p m3 sg
                self.czas_przeszły.liczba_pojedyncza.pierwsza_osoba.f,   # przeszły 1p f sg
                self.czas_przeszły.liczba_pojedyncza.pierwsza_osoba.n,   # przeszły 1p n sg
                self.czas_przeszły.liczba_pojedyncza.druga_osoba.m1,     # przeszły 2p m1 sg
                self.czas_przeszły.liczba_pojedyncza.druga_osoba.m2,     # przeszły 2p m2 sg
                self.czas_przeszły.liczba_pojedyncza.druga_osoba.m3,     # przeszły 2p m3 sg
                self.czas_przeszły.liczba_pojedyncza.druga_osoba.f,      # przeszły 2p f sg
                self.czas_przeszły.liczba_pojedyncza.druga_osoba.n,      # przeszły 2p n sg
                self.czas_przeszły.liczba_pojedyncza.trzecia_osoba.m1,   # przeszły 3p m1 sg
                self.czas_przeszły.liczba_pojedyncza.trzecia_osoba.m2,   # przeszły 3p m2 sg
                self.czas_przeszły.liczba_pojedyncza.trzecia_osoba.m3,   # przeszły 3p m3 sg
                self.czas_przeszły.liczba_pojedyncza.trzecia_osoba.f,    # przeszły 3p f sg
                self.czas_przeszły.liczba_pojedyncza.trzecia_osoba.n,    # przeszły 3p n sg
                self.czas_przeszły.liczba_mnoga.pierwsza_osoba.m1,       # przeszły 1p m1 pl
                self.czas_przeszły.liczba_mnoga.pierwsza_osoba.reszta,   # przeszły 1p r  pl
                self.czas_przeszły.liczba_mnoga.druga_osoba.m1,          # przeszły 2p m1 pl
                self.czas_przeszły.liczba_mnoga.druga_osoba.reszta,      # przeszły 2p r  pl
                self.czas_przeszły.liczba_mnoga.trzecia_osoba.m1,        # przeszły 3p m1 pl
                self.czas_przeszły.liczba_mnoga.trzecia_osoba.reszta,    # przeszły 3p r pl

                self.czas_przyszły.liczba_pojedyncza.pierwsza_osoba,     # przyszły 1p m1 sg
                "",                                                      # przyszły 1p m2 sg
                "",                                                      # przyszły 1p m3 sg
                "",                                                      # przyszły 1p f sg
                "",                                                      # przyszły 1p n sg
                self.czas_przyszły.liczba_pojedyncza.druga_osoba,        # przyszły 2p m1 sg
                "",                                                      # przyszły 2p m2 sg
                "",                                                      # przyszły 2p m3 sg
                "",                                                      # przyszły 2p f sg
                "",                                                      # przyszły 2p n sg
                self.czas_przyszły.liczba_pojedyncza.trzecia_osoba,      # przyszły 3p m1 sg
                "",                                                      # przyszły 3p m2 sg
                "",                                                      # przyszły 3p m3 sg
                "",                                                      # przyszły 3p f sg
                "",                                                      # przyszły 3p n sg
                self.czas_przyszły.liczba_mnoga.pierwsza_osoba,          # przyszły 1p m1 pl
                "",                                                      # przyszły 1p r  pl
                self.czas_przyszły.liczba_mnoga.druga_osoba,             # przyszły 2p m1 pl
                "",                                                      # przyszły 2p r  pl
                self.czas_przyszły.liczba_mnoga.trzecia_osoba,           # przyszły 3p m1 pl
                "",                                                      # przyszły 3p r pl
            )
        else:
            raise ValueError("Invalid verb forms")


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
            liczba_mnoga=_CaseForms(
                mianownik="",
                dopełniacz="",
                celownik="",
                biernik="",
                miejscownik="",
                narzędnik="",
                wołacz="",
            ),
            liczba_pojedyncza=_CaseForms(
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
