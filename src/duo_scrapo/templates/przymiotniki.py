from attrs import asdict
from genanki.model import Model

from duo_scrapo.words.adjectives import AdjectiveForms
from ..Morf import VerbForms  # noqa: TID252
from . import AnkiTemplate, cond, dedent, end_cond, field, front, humanize_gender, humanize_number


def humanize_col_name(col_name: str) -> str:
    match col_name.split("_"):
        case [(number), (gender), (case)]:
            return " ".join(
                [
                    humanize_gender(gender),
                    humanize_number(number),
                    case,
                ]
            )
        case [(number), (gender), (case)]:
            return " ".join(
                [
                    humanize_gender(gender),
                    humanize_number(number),
                    f"({case})",
                ]
            )
        case _:
            return col_name.capitalize()


class TplA(AnkiTemplate):
    pass


class TplB(AnkiTemplate):
    pass


def _make_declension_table() -> str:
    return dedent("""
    """)


def _make_template(col: str):
    return AnkiTemplate(
        name=humanize_col_name(col),
        qfmt=dedent(
            f"""
            {cond(col)}
                {field('bezokolicznik')} ({humanize_col_name(col)})
                <p>{field(f"type:{col}")}</p>
            {end_cond(col)}
            """
        ),
        afmt=dedent(
            f"""
            {front()}

            <hr id="answer">

            <p class="field-{col}">
                {field(col)}
            </p>
            <p class="field-en">
                {field("en")}
            </p>
            <hr id="conjugation">
            {_make_declension_table()}
            """
        ),
    )


templates = [
    _make_template(col)
    for col in filter(
        lambda name: name not in {"en", "pl"},
        VerbForms.get_cols(),
    )
]


MODEL_ID_PRZYMIOTNIKI = 2120170845

model = Model(
    model_id=MODEL_ID_PRZYMIOTNIKI,
    name="Przymiotniki",
    fields=[
        {"name": col}
        for col in ("en", "pl", *AdjectiveForms.get_cols())
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
