from collections.abc import Callable
from typing import NamedTuple, Self
from attrs import define, asdict
from genanki.model import Model

from duo_scrapo.templates import AnkiTemplate, dedent
from duo_scrapo.words import SupportsEmpty


class CsvRow(NamedTuple):
    form: str


@define
class AdverbForms(SupportsEmpty[str]):
    form: str

    @classmethod
    def empty(cls, empty: Callable[[], str]) -> Self:
        return cls(form=empty())

    @staticmethod
    def get_cols() -> CsvRow:
        return CsvRow(form="form")

    def to_rows(self) -> CsvRow:
        return CsvRow(form=self.form)

    def as_dict(self) -> dict[str, str]:
        return dict(zip(self.get_cols(), self.to_rows(), strict=True))


templates = [
    AnkiTemplate(
        name="Adverb",
        qfmt=dedent("""
            {{en}}
        """),
        afmt=dedent("""
            {{FrontSide}}
            <hr id="answer">
            {{pl}}
        """),
    )
]


MODEL_ID_PRZYSŁÓWKI = 2103738595

model = Model(
    model_id=MODEL_ID_PRZYSŁÓWKI,
    name="Przysłówki",
    fields=[
        {"name": col}
        for col in ("en", "pl", *AdverbForms.get_cols())
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
