from collections.abc import Callable
from typing import Self
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


@define
class NounForms:
    rodzaj: Tag
    liczba_pojedyncza: CaseForms
    liczba_mnoga: CaseForms

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
