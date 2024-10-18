import itertools
from collections.abc import Callable, Iterable
from typing import NamedTuple, Self, TypeIs

from attrs import asdict, define
from genanki.model import Model

from duo_scrapo.tag import Tag
from duo_scrapo.templates import AnkiTemplate, dedent, field
from duo_scrapo.słowa import FormyPrzypadków


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
class FormyRzeczowników:
    rodzaj: Tag
    liczba_pojedyncza: FormyPrzypadków[str]
    liczba_mnoga: FormyPrzypadków[str]

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
    def empty(cls, empty: Callable[[], str]) -> Self:
        return cls(
            rodzaj=Tag(frozenset({})),
            liczba_pojedyncza=FormyPrzypadków.empty(empty),
            liczba_mnoga=FormyPrzypadków.empty(empty),
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
        FormyRzeczowników.get_cols(),
    ),
)

MODEL_ID_RZECZOWNIKI = 2026523460

model = Model(
    model_id=MODEL_ID_RZECZOWNIKI,
    name="Rzeczowniki",
    fields=[
        {"name": col}
        for col in ("en", "pl", *FormyRzeczowników.get_cols())
    ],
    templates=[
        asdict(a)
        for a in templates
    ],
    css=dedent("""
        table {
            font-size: .75rem;
            line-height: 1rem;
            margin-bottom: .5rem;
            margin-top: .5rem;
            width: 100%;
        }
        th { background-color: silver; }
        td { border: 1px solid black; }

    """)
)
