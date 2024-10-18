from collections.abc import Callable
from typing import NamedTuple

from attrs import asdict, define
from genanki.model import Model

from duo_scrapo.templates import AnkiTemplate, cond, dedent, end_cond, field, front
from duo_scrapo.słowa import SupportsAnkiExport, SupportsEmpty


class CsvRow(NamedTuple):
    preposition: str
    takes_mianownik: str
    takes_dopełniacz: str
    takes_celownik: str
    takes_biernik: str
    takes_miejscownik: str
    takes_narzędnik: str
    takes_wołacz: str
    takes_extra: str


@define
class BasePrepositionForms:
    preposition: str
    takes_mianownik: bool
    takes_dopełniacz: bool
    takes_celownik: bool
    takes_biernik: bool
    takes_miejscownik: bool
    takes_narzędnik: bool
    takes_wołacz: bool
    takes_extra: str


@define
class FormyPrzyimków(BasePrepositionForms, SupportsAnkiExport, SupportsEmpty[BasePrepositionForms]):
    @classmethod
    def get_cols(cls):
        return (
            "preposition",
            "takes_mianownik",
            "takes_dopełniacz",
            "takes_celownik",
            "takes_biernik",
            "takes_miejscownik",
            "takes_narzędnik",
            "takes_wołacz",
            "takes_extra",
        )

    def to_rows(self):
        return CsvRow(
            self.preposition,
            "1" if self.takes_mianownik else "",
            "1" if self.takes_dopełniacz else "",
            "1" if self.takes_celownik else "",
            "1" if self.takes_biernik else "",
            "1" if self.takes_miejscownik else "",
            "1" if self.takes_narzędnik else "",
            "1" if self.takes_wołacz else "",
            "1" if self.takes_extra else "",
        )

    def as_dict(self) -> dict[str, str]:
        return dict(zip(self.get_cols(), self.to_rows(), strict=True))

    @classmethod
    def empty(cls, empty: Callable[[], BasePrepositionForms]):
        e = empty()
        return cls(
            preposition=e.preposition,
            takes_mianownik=e.takes_mianownik,
            takes_dopełniacz=e.takes_dopełniacz,
            takes_celownik=e.takes_celownik,
            takes_biernik=e.takes_biernik,
            takes_miejscownik=e.takes_miejscownik,
            takes_narzędnik=e.takes_narzędnik,
            takes_wołacz=e.takes_wołacz,
            takes_extra=e.takes_extra,
        )


def humanize_col_name(col_name: str) -> str:
    if col_name == "takes_extra":
        return "+"
    elif col_name == "preposition":
        return "takes ... ?"

    match col_name.split("_"):
        case [_, (case)]:
            return f"+{case}"
        case _:
            return col_name


def _make_template(col: str):
    return AnkiTemplate(
        name=humanize_col_name(col),
        qfmt=dedent(
            f"""
            {cond(col)}
                {field('preposition')} ({humanize_col_name(col)})
            {end_cond(col)}
            """
        ),
        afmt=dedent(
            f"""
            {front()}

            <hr id="answer">

            <p class="field-en">
                {field("en")}

                {cond("takes_extra")}
                <div class="field-takes_extra">
                    {field("preposition")} (+{field("takes_extra")})
                </div>
                {end_cond("takes_extra")}

                <ul>


                    {cond("takes_mianownik")}
                    <li>{field("preposition")} (+mian)</li>
                    {end_cond("takes_mianownik")}

                    {cond("takes_dopełniacz")}
                    <li>{field("preposition")} (+dop)</li>
                    {end_cond("takes_dopełniacz")}

                    {cond("takes_celownik")}
                    <li>{field("preposition")} (+cel)</li>
                    {end_cond("takes_celownik")}

                    {cond("takes_biernik")}
                    <li>{field("preposition")} (+bier)</li>
                    {end_cond("takes_biernik")}

                    {cond("takes_miejscownik")}
                    <li>{field("preposition")} (+miejs)</li>
                    {end_cond("takes_miejscownik")}

                    {cond("takes_miejscownik")}
                    <li>{field("preposition")} (+narz)</li>
                    {end_cond("takes_miejscownik")}

                    {cond("takes_wołacz")}
                    <li>{field("preposition")} (+woł)</li>
                    {end_cond("takes_wołacz")}
                </ul>
            </p>
            """
        ),
    )


templates = [
    _make_template(col)
    for col in filter(
        lambda name: name not in {"en", "pl"},
        FormyPrzyimków.get_cols(),
    )
]


MODEL_ID_PRZYIMKI = 2142396272

model = Model(
    model_id=MODEL_ID_PRZYIMKI,
    name="Przyimki",
    fields=[
        {"name": col}
        for col in ("en", "pl", *FormyPrzyimków.get_cols())
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
