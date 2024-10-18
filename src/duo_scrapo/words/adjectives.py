from typing import NamedTuple
from attrs import define

from duo_scrapo.words import CaseForms, Gendered, GenderedPlural, GenderedSingular
from attrs import asdict
from genanki.model import Model

from duo_scrapo.templates import AnkiTemplate, cond, dedent, end_cond, field, front, humanize_gender, humanize_number


class CsvRow(NamedTuple):
    lp_m1_mianownik: str
    lp_m1_dopełniacz: str
    lp_m1_celownik: str
    lp_m1_biernik: str
    lp_m1_narzędnik: str
    lp_m1_miejscownik: str
    lp_m1_wołacz: str

    lp_m2_mianownik: str
    lp_m2_dopełniacz: str
    lp_m2_celownik: str
    lp_m2_biernik: str
    lp_m2_narzędnik: str
    lp_m2_miejscownik: str
    lp_m2_wołacz: str

    lp_m3_mianownik: str
    lp_m3_dopełniacz: str
    lp_m3_celownik: str
    lp_m3_biernik: str
    lp_m3_narzędnik: str
    lp_m3_miejscownik: str
    lp_m3_wołacz: str

    lp_f_mianownik: str
    lp_f_dopełniacz: str
    lp_f_celownik: str
    lp_f_biernik: str
    lp_f_narzędnik: str
    lp_f_miejscownik: str
    lp_f_wołacz: str

    lp_n_mianownik: str
    lp_n_dopełniacz: str
    lp_n_celownik: str
    lp_n_biernik: str
    lp_n_narzędnik: str
    lp_n_miejscownik: str
    lp_n_wołacz: str

    lm_m1_mianownik: str
    lm_m1_dopełniacz: str
    lm_m1_celownik: str
    lm_m1_biernik: str
    lm_m1_narzędnik: str
    lm_m1_miejscownik: str
    lm_m1_wołacz: str

    lm_r_mianownik: str
    lm_r_dopełniacz: str
    lm_r_celownik: str
    lm_r_biernik: str
    lm_r_narzędnik: str
    lm_r_miejscownik: str
    lm_r_wołacz: str


@define
class AdjectiveForms(Gendered[CaseForms]):
    liczba_pojedyncza: GenderedSingular[CaseForms[str]]
    liczba_mnoga: GenderedPlural[CaseForms[str]]

    @staticmethod
    def get_cols() -> CsvRow:
        return CsvRow(
            "lp_m1_mianownik",
            "lp_m1_dopełniacz",
            "lp_m1_celownik",
            "lp_m1_biernik",
            "lp_m1_narzędnik",
            "lp_m1_miejscownik",
            "lp_m1_wołacz",

            "lp_m2_mianownik",
            "lp_m2_dopełniacz",
            "lp_m2_celownik",
            "lp_m2_biernik",
            "lp_m2_narzędnik",
            "lp_m2_miejscownik",
            "lp_m2_wołacz",

            "lp_m3_mianownik",
            "lp_m3_dopełniacz",
            "lp_m3_celownik",
            "lp_m3_biernik",
            "lp_m3_narzędnik",
            "lp_m3_miejscownik",
            "lp_m3_wołacz",

            "lp_f_mianownik",
            "lp_f_dopełniacz",
            "lp_f_celownik",
            "lp_f_biernik",
            "lp_f_narzędnik",
            "lp_f_miejscownik",
            "lp_f_wołacz",

            "lp_n_mianownik",
            "lp_n_dopełniacz",
            "lp_n_celownik",
            "lp_n_biernik",
            "lp_n_narzędnik",
            "lp_n_miejscownik",
            "lp_n_wołacz",

            "lm_m1_mianownik",
            "lm_m1_dopełniacz",
            "lm_m1_celownik",
            "lm_m1_biernik",
            "lm_m1_narzędnik",
            "lm_m1_miejscownik",
            "lm_m1_wołacz",

            "lm_r_mianownik",
            "lm_r_dopełniacz",
            "lm_r_celownik",
            "lm_r_biernik",
            "lm_r_narzędnik",
            "lm_r_miejscownik",
            "lm_r_wołacz",
        )

    def as_dict(self) -> dict[str, str]:
        return dict(zip(self.get_cols(), self.to_rows(), strict=True))

    def to_rows(self) -> CsvRow:
        return CsvRow(
            self.liczba_pojedyncza.m1.mianownik,      # "lp_m1_mianownik",
            self.liczba_pojedyncza.m1.dopełniacz,     # "lp_m1_dopełniacz",
            self.liczba_pojedyncza.m1.celownik,       # "lp_m1_celownik",
            self.liczba_pojedyncza.m1.biernik,        # "lp_m1_biernik",
            self.liczba_pojedyncza.m1.narzędnik,      # "lp_m1_narzędnik",
            self.liczba_pojedyncza.m1.miejscownik,    # "lp_m1_miejscownik",
            self.liczba_pojedyncza.m1.wołacz,         # "lp_m1_wołacz",

            self.liczba_pojedyncza.m2.mianownik,      # "lp_m2_mianownik",
            self.liczba_pojedyncza.m2.dopełniacz,     # "lp_m2_dopełniacz",
            self.liczba_pojedyncza.m2.celownik,       # "lp_m2_celownik",
            self.liczba_pojedyncza.m2.biernik,        # "lp_m2_biernik",
            self.liczba_pojedyncza.m2.narzędnik,      # "lp_m2_narzędnik",
            self.liczba_pojedyncza.m2.miejscownik,    # "lp_m2_miejscownik",
            self.liczba_pojedyncza.m2.wołacz,         # "lp_m2_wołacz",

            self.liczba_pojedyncza.m3.mianownik,      # "lp_m3_mianownik",
            self.liczba_pojedyncza.m3.dopełniacz,     # "lp_m3_dopełniacz",
            self.liczba_pojedyncza.m3.celownik,       # "lp_m3_celownik",
            self.liczba_pojedyncza.m3.biernik,        # "lp_m3_biernik",
            self.liczba_pojedyncza.m3.narzędnik,      # "lp_m3_narzędnik",
            self.liczba_pojedyncza.m3.miejscownik,    # "lp_m3_miejscownik",
            self.liczba_pojedyncza.m3.wołacz,         # "lp_m3_wołacz",

            self.liczba_pojedyncza.f.mianownik,       # "lp_f_mianownik",
            self.liczba_pojedyncza.f.dopełniacz,      # "lp_f_dopełniacz",
            self.liczba_pojedyncza.f.celownik,        # "lp_f_celownik",
            self.liczba_pojedyncza.f.biernik,         # "lp_f_biernik",
            self.liczba_pojedyncza.f.narzędnik,       # "lp_f_narzędnik",
            self.liczba_pojedyncza.f.miejscownik,     # "lp_f_miejscownik",
            self.liczba_pojedyncza.f.wołacz,          # "lp_f_wołacz",

            self.liczba_pojedyncza.n.mianownik,       # "lp_n_mianownik",
            self.liczba_pojedyncza.n.dopełniacz,      # "lp_n_dopełniacz",
            self.liczba_pojedyncza.n.celownik,        # "lp_n_celownik",
            self.liczba_pojedyncza.n.biernik,         # "lp_n_biernik",
            self.liczba_pojedyncza.n.narzędnik,       # "lp_n_narzędnik",
            self.liczba_pojedyncza.n.miejscownik,     # "lp_n_miejscownik",
            self.liczba_pojedyncza.n.wołacz,          # "lp_n_wołacz",

            self.liczba_mnoga.m1.mianownik,           # "lm_m1_mianownik",
            self.liczba_mnoga.m1.dopełniacz,          # "lm_m1_dopełniacz",
            self.liczba_mnoga.m1.celownik,            # "lm_m1_celownik",
            self.liczba_mnoga.m1.biernik,             # "lm_m1_biernik",
            self.liczba_mnoga.m1.narzędnik,           # "lm_m1_narzędnik",
            self.liczba_mnoga.m1.miejscownik,         # "lm_m1_miejscownik",
            self.liczba_mnoga.m1.wołacz,              # "lm_m1_wołacz",

            self.liczba_mnoga.reszta.mianownik,       # "lm_r_mianownik",
            self.liczba_mnoga.reszta.dopełniacz,      # "lm_r_dopełniacz",
            self.liczba_mnoga.reszta.celownik,        # "lm_r_celownik",
            self.liczba_mnoga.reszta.biernik,         # "lm_r_biernik",
            self.liczba_mnoga.reszta.narzędnik,       # "lm_r_narzędnik",
            self.liczba_mnoga.reszta.miejscownik,     # "lm_r_miejscownik",
            self.liczba_mnoga.reszta.wołacz,          # "lm_r_wołacz",
        )


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
        AdjectiveForms.get_cols(),
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
