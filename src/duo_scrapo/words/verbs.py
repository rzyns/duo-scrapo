from collections.abc import Callable
from typing import NamedTuple, Self, TypeIs
from attrs import define, field

from duo_scrapo.tag import Tag

import attr

from duo_scrapo.words.forms import Gendered, GenderedPlural, GenderedSingular, Numbered


@define
class VerbPersonForms[T = str]:  # noqa: E251
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

    is_perfect: str
    is_imperfect: str


@define
class VerbForms:
    aspekt: Tag
    bezokolicznik: str = field(default="")

    # Present tense _form_
    _czas_teraźniejszy: Numbered[VerbPersonForms[str], VerbPersonForms[str]] = field(
        default=Numbered[VerbPersonForms[str], VerbPersonForms[str]].empty(
            VerbPersonForms[str].empty(""),
            VerbPersonForms[str].empty(""),
        )
    )

    @property
    def czas_teraźniejszy(self) -> Numbered[VerbPersonForms[str], VerbPersonForms[str]]:
        if self.aspekt == Tag.PERFECTIVE:
            return Numbered[VerbPersonForms[str], VerbPersonForms[str]].empty(
                empty_lp=VerbPersonForms[str].empty(""),
                empty_lm=VerbPersonForms[str].empty(""),
            )
        return self._czas_teraźniejszy

    bezosobnik: str = field(default="")

    rdzeń_czasu_przeszłego: Gendered[str] = field(default=Gendered[str].empty(""))

    # mówił  = praet:sg:m1.m2.m3:imperf
    # mówiła = praet:sg:f:imperf
    # mówiło = praet:sg:n:imperf
    # mówili = praet:pl:m1:imperf
    # mówiły = praet:pl:m2.m3.f.n:imperf

    @property
    def czas_przeszły(self) -> Numbered[VerbPersonForms[GenderedSingular[str]], VerbPersonForms[GenderedPlural[str]]]:
        return Numbered(
            liczba_pojedyncza=VerbPersonForms(
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
            liczba_mnoga=VerbPersonForms(
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
    def czas_przyszły(self) -> Numbered[VerbPersonForms[str], VerbPersonForms[str]] | Numbered[VerbPersonForms[GenderedSingular[str]], VerbPersonForms[GenderedPlural[str]]]:
        if self.is_perfective():
            return self._czas_teraźniejszy

        return Numbered(
            liczba_pojedyncza=VerbPersonForms(
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
            liczba_mnoga=VerbPersonForms(
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

    def is_perfective(self, forms: None | Numbered[VerbPersonForms[str], VerbPersonForms[str]] | Numbered[VerbPersonForms[GenderedSingular[str]], VerbPersonForms[GenderedPlural[str]]] = None) -> TypeIs[Numbered[VerbPersonForms[str], VerbPersonForms[str]]]:
        return bool(self.aspekt & Tag.PERFECTIVE)

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

            "_is_perfect",
            "_is_imperfect",
        )

    def as_dict(self) -> dict[str, str]:
        return dict(zip(self.get_cols(), self.to_rows(), strict=True))

    def to_rows(self) -> CsvRow:
        if not self.is_perfective(self.czas_przyszły):
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

                "",                                                       # _is_perfect
                "1",                                                      # _is_imperfect
             )
        else:
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

                "1",                                                     # "_is_perfect",
                "",                                                      # "_is_imperfect",
            )

    class InvalidVerbFormError(Exception):
        """Raised when the verb form is invalid"""
        def __init__(self, form: "VerbForms"):
            super().__init__(f"Invalid verb form: {form.bezokolicznik}")
