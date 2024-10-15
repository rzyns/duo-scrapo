from collections.abc import Callable
from typing import NamedTuple, Self
from attrs import define
import attr

from duo_scrapo.tag import Tag
from duo_scrapo.words.forms import SupportsEmpty


@define
class CaseForms[T = str](SupportsEmpty[T]):  # noqa: E251
    mianownik: T
    dopełniacz: T
    celownik: T
    biernik: T
    miejscownik: T
    narzędnik: T
    wołacz: T

    @classmethod
    def empty(cls, empty: T | Callable[[], T]) -> Self:
        return cls(
            mianownik=empty if not callable(empty) else empty(),
            dopełniacz=empty if not callable(empty) else empty(),
            celownik=empty if not callable(empty) else empty(),
            biernik=empty if not callable(empty) else empty(),
            miejscownik=empty if not callable(empty) else empty(),
            narzędnik=empty if not callable(empty) else empty(),
            wołacz=empty if not callable(empty) else empty(),
        )

    def is_empty(self) -> bool:
        return not any(attr.asdict(self).values())


class CsvRow(NamedTuple):
    rodzaj: str
    lp_mianownik: str
    lp_dopełniacz: str
    lp_celownik: str
    lp_biernik: str
    lp_narzędnik: str
    lp_miejscownik: str
    lp_wołacz: str
    lm_mianownik: str
    lm_dopełniacz: str
    lm_celownik: str
    lm_biernik: str
    lm_narzędnik: str
    lm_miejscownik: str
    lm_wołacz: str


@define
class NounForms:
    rodzaj: Tag
    liczba_pojedyncza: CaseForms
    liczba_mnoga: CaseForms

    @staticmethod
    def get_cols() -> CsvRow:
        return CsvRow(
            "rodzaj",
            "lp_mianownik",
            "lp_dopełniacz",
            "lp_celownik",
            "lp_biernik",
            "lp_narzędnik",
            "lp_miejscownik",
            "lp_wołacz",
            "lm_mianownik",
            "lm_dopełniacz",
            "lm_celownik",
            "lm_biernik",
            "lm_narzędnik",
            "lm_miejscownik",
            "lm_wołacz",
        )

    def as_dict(self) -> dict[str, str]:
        return dict(zip(self.get_cols(), self.to_rows(), strict=True))

    def to_rows(self) -> CsvRow:
        return CsvRow(
            rodzaj=str(self.rodzaj),
            lp_mianownik=self.liczba_pojedyncza.mianownik,
            lp_dopełniacz=self.liczba_pojedyncza.dopełniacz,
            lp_celownik=self.liczba_pojedyncza.celownik,
            lp_biernik=self.liczba_pojedyncza.biernik,
            lp_narzędnik=self.liczba_pojedyncza.narzędnik,
            lp_miejscownik=self.liczba_pojedyncza.miejscownik,
            lp_wołacz=self.liczba_pojedyncza.wołacz,

            lm_mianownik=self.liczba_mnoga.mianownik,
            lm_dopełniacz=self.liczba_mnoga.dopełniacz,
            lm_celownik=self.liczba_mnoga.celownik,
            lm_biernik=self.liczba_mnoga.biernik,
            lm_narzędnik=self.liczba_mnoga.narzędnik,
            lm_miejscownik=self.liczba_mnoga.miejscownik,
            lm_wołacz=self.liczba_mnoga.wołacz,
        )

    @classmethod
    def empty(cls, empty: str | Callable[[], str]) -> Self:
        return cls(
            rodzaj=Tag(frozenset({})),
            liczba_pojedyncza=CaseForms.empty(empty),
            liczba_mnoga=CaseForms.empty(empty),
        )

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
