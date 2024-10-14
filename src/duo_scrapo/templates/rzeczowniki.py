# rodzaj
# lp_mianownik
# lp_dopełniacz
# lp_celownik
# lp_biernik
# lp_narzędnik
# lp_miejscownik
# lp_wołacz
# lm_mianownik
# lm_dopełniacz
# lm_celownik
# lm_biernik
# lm_narzędnik
# lm_miejscownik
# lm_wołacz


import itertools
from collections.abc import Callable, Iterable
from typing import TypeIs

from ..Morf import NounForms  # noqa: TID252
from . import AnkiTemplate, dedent, field


def humanize(col: str):
    match col:
        case "lp_mianownik":
            return "lp mianownik"
        case "lp_dopełniacz":
            return "lp dopełniacz"
        case "lp_celownik":
            return "lp celownik"
        case "lp_biernik":
            return "lp biernik"
        case "lp_narzędnik":
            return "lp narzędnik"
        case "lp_miejscownik":
            return "lp miejscownik"
        case "lp_wołacz":
            return "lp wołacz"
        case "lm_mianownik":
            return "lm mianownik"
        case "lm_dopełniacz":
            return "lm dopełniacz"
        case "lm_celownik":
            return "lm celownik"
        case "lm_biernik":
            return "lm biernik"
        case "lm_narzędnik":
            return "lm narzędnik"
        case "lm_miejscownik":
            return "lm miejscownik"
        case "lm_wołacz":
            return "lm wołacz"
        case _:
            return col


def _make_to_polish_template(col: str):
    if col in {"lp_mianownik", "rodzaj"}:
        return None

    return AnkiTemplate(
        name=col,
        qfmt=dedent(
            f"""
            {field(f"#{col}")}
            {field('en')} ({humanize(col)})
            <p>{field(f"type:{col}")}</p>
            {field(f"/{col}")}
            """
        ),
        afmt=dedent(
            f"""
            {field("FrontSide")}
            <hr id="answer">
            <p class="field-{col}">
                {field(col)} ({field("rodzaj")})
            </p>
            <hr id="declension">
            {_make_declension_table()}
            """
        ),
    )


def _make_declension_table() -> str:
    return dedent(
        f"""
        <table class="declension">
            <tr>
                <th></th>
                <th>liczba pojedyncza</th>
                <th>liczba mnoga</th>
            </tr>
            <tr>
                <th>mianownik</th> <td>{field("lp_mianownik")}</td> <td>{field("lm_mianownik")}</td>
            </tr>
            <tr>
                <th>dopełniacz</th> <td>{field("lp_dopełniacz")}</td> <td>{field("lm_dopełniacz")}</td>
            </tr>
            <tr>
                <th>celownik</th> <td>{field("lp_celownik")}</td> <td>{field("lm_celownik")}</td>
            </tr>
            <tr>
                <th>biernik</th> <td>{field("lp_biernik")}</td> <td>{field("lm_biernik")}</td>
            </tr>
            <tr>
                <th>narzędnik</th> <td>{field("lp_narzędnik")}</td> <td>{field("lp_narzędnik")}</td>
            </tr>
            <tr>
                <th>miejscownik</th> <td>{field("lp_miejscownik")}</td> <td>{field("lm_miejscownik")}</td>
            </tr>
            <tr>
                <th>wołacz</th> <td>{field("lp_wołacz")}</td> <td>{field("lm_wołacz")}</td>
            </tr>
        </table>
        """
    )


def _make_to_english_template(col: str):
    if col == "rodzaj":
        return None

    return AnkiTemplate(
        name=col,
        qfmt=dedent(
            f"""
            {field(f"#{col}")}
            {field(col)}
            {field(f"/{col}")}
            """
        ),
        afmt=dedent(
            f"""
            {field("FrontSide")}
            <hr id="answer">
            <p class="field-en">
                {field("en")}<br/>
                {humanize(col)} ({field("rodzaj")})
            </p>
            <hr id="declension">
            {_make_declension_table()}
            """
        ),
    )


def not_none[T](x: T | None) -> TypeIs[T]:
    return x is not None


def _make_template(col: str) -> Iterable[AnkiTemplate]:
    return filter(
        not_none,
        [
            _make_to_polish_template(col),
            _make_to_english_template(col),
        ]
    )


def flatmap[A, B](
    func: Callable[[A], Iterable[B]], *iterable: Iterable[A | Iterable[A]]
) -> Iterable[B]:
    return itertools.chain[B].from_iterable(map(func, *iterable))


templates = flatmap(
    _make_template,
    filter(
        lambda name: name not in {"en", "pl"},
        NounForms.get_cols(),
    ),
)
