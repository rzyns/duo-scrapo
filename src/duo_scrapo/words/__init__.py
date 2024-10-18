from abc import abstractmethod
from typing import Protocol, Self
from collections.abc import Callable

import attr
from attrs import define, field


class SupportsEmpty[T](Protocol):
    @classmethod
    @abstractmethod
    def empty(cls, empty: Callable[[], T]) -> Self: ...


class SupportsAnkiExport(Protocol):
    @classmethod
    @abstractmethod
    def get_cols(cls) -> tuple[str, ...]: ...

    @abstractmethod
    def as_dict(self) -> dict[str, str]: ...

    @abstractmethod
    def to_rows(self) -> tuple[str, ...]: ...


@define
class Numbered[T, U]:
    liczba_pojedyncza: T
    liczba_mnoga: U

    @classmethod
    def empty(cls, empty_lp: Callable[[], T], empty_lm: Callable[[], U]) -> Self:
        return cls(
            liczba_pojedyncza=empty_lp(),
            liczba_mnoga=empty_lm(),
        )


@define
class GenderedSingular[T]:
    m1: T = field()
    m2: T = field()
    m3: T = field()
    f:  T = field()
    n:  T = field()

    @classmethod
    def empty(cls, empty: Callable[[], T]) -> Self:
        return cls(
            m1=empty if not callable(empty) else empty(),
            m2=empty if not callable(empty) else empty(),
            m3=empty if not callable(empty) else empty(),
            f=empty if not callable(empty) else empty(),
            n=empty if not callable(empty) else empty(),
        )

    def is_empty(self) -> bool:
        return not any(attr.asdict(self).values())


@define
class GenderedPlural[T]:
    m1: T = field(default=None)
    reszta: T = field(default=None)

    @classmethod
    def empty(cls, empty: Callable[[], T]) -> Self:
        return cls(
            m1=empty if not callable(empty) else empty(),
            reszta=empty if not callable(empty) else empty(),
        )


@define
class Gendered[T]:
    liczba_pojedyncza: GenderedSingular[T] = field()
    liczba_mnoga: GenderedPlural[T] = field()

    @classmethod
    def empty(cls, empty: Callable[[], T]) -> Self:
        return cls(
            liczba_pojedyncza=GenderedSingular[T].empty(empty),
            liczba_mnoga=GenderedPlural[T].empty(empty),
        )


class HasGender[T = str](Protocol):
    liczba_pojedyncza: GenderedSingular[T]
    liczba_mnoga: GenderedPlural[T]

    @classmethod
    def empty(cls, empty: T | Callable[[], T]) -> Self: ...


@define
class HasCase:
    mianownik: str
    dopełniacz: str
    celownik: str
    biernik: str
    miejscownik: str
    narzędnik: str
    wołacz: str

    @classmethod
    def empty(cls, empty: str | Callable[[], str]) -> Self:
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
class CaseForms[T = str](SupportsEmpty[T]):
    mianownik: T
    dopełniacz: T
    celownik: T
    biernik: T
    miejscownik: T
    narzędnik: T
    wołacz: T

    @classmethod
    def empty(cls, empty: Callable[[], T]) -> Self:
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
