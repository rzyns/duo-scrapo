# aspekt: str

# bezokolicznik: str

# teraz_sg_1p: str
# teraz_sg_2p: str
# teraz_sg_3p: str
# teraz_pl_1p: str
# teraz_pl_2p: str
# teraz_pl_3p: str

# przeszły_sg_1p_m1: str
# przeszły_sg_1p_m2: str
# przeszły_sg_1p_m3: str
# przeszły_sg_1p_f: str
# przeszły_sg_1p_n: str
# przeszły_sg_2p_m1: str
# przeszły_sg_2p_m2: str
# przeszły_sg_2p_m3: str
# przeszły_sg_2p_f: str
# przeszły_sg_2p_n: str
# przeszły_sg_3p_m1: str
# przeszły_sg_3p_m2: str
# przeszły_sg_3p_m3: str
# przeszły_sg_3p_f: str
# przeszły_sg_3p_n: str
# przeszły_pl_1p_m1: str
# przeszły_pl_1p_r: str
# przeszły_pl_2p_m1: str
# przeszły_pl_2p_r: str
# przeszły_pl_3p_m1: str
# przeszły_pl_3p_r: str

# przyszły_sg_1p_m1: str
# przyszły_sg_1p_m2: str
# przyszły_sg_1p_m3: str
# przyszły_sg_1p_f: str
# przyszły_sg_1p_n: str
# przyszły_sg_2p_m1: str
# przyszły_sg_2p_m2: str
# przyszły_sg_2p_m3: str
# przyszły_sg_2p_f: str
# przyszły_sg_2p_n: str
# przyszły_sg_3p_m1: str
# przyszły_sg_3p_m2: str
# przyszły_sg_3p_m3: str
# przyszły_sg_3p_f: str
# przyszły_sg_3p_n: str
# przyszły_pl_1p_m1: str
# przyszły_pl_1p_r: str
# przyszły_pl_2p_m1: str
# przyszły_pl_2p_r: str
# przyszły_pl_3p_m1: str
# przyszły_pl_3p_r: str


from attrs import define

from duo_scrapo.Morf import VerbForms


@define
class AnkiTemplate:
    name: str
    qfmt: str
    afmt: str


def humanize_tense(tense: str) -> str:
    match tense:
        case "teraz":
            return "Present"
        case "przeszły":
            return "Past"
        case "przyszły":
            return "Future"
        case _:
            return tense.capitalize()


def humanize_number(number: str) -> str:
    match number:
        case "sg":
            return "Singular"
        case "pl":
            return "Plural"
        case _:
            return number.capitalize()


def humanize_person(person: str) -> str:
    match person:
        case "1p":
            return "1st Person"
        case "2p":
            return "2nd Person"
        case "3p":
            return "3rd Person"
        case _:
            return person.capitalize()


def humanize_gender(gender: str) -> str:  # noqa: PLR0911
    match gender:
        case "m1":
            return "Masculine Virile"
        case "m2":
            return "Masculine Non-Virile"
        case "m3":
            return "Masculine Inanimate"
        case "f":
            return "Feminine"
        case "n":
            return "Neuter"
        case "r":
            return "Common"
        case _:
            return gender.capitalize()


def humanize_col_name(col_name: str) -> str:
    match col_name.split("_"):
        case [(tense), (number), (person), (gender)]:
            return " ".join([
                humanize_tense(tense),
                humanize_number(number),
                humanize_person(person),
                humanize_gender(gender),
            ])
        case [(tense), (number), (person)]:
            return " ".join([
                humanize_tense(tense),
                humanize_number(number),
                humanize_person(person),
            ])
        case _:
            return col_name.capitalize()


def _make_template(col: str):
    match col:
        case "bezokolicznik":
            return AnkiTemplate(
                name="Infinitive",
                qfmt="{{en}} (Infinitive)",
                afmt="{{FrontSide}}<hr id=\"answer\">{{{{bezokolicznik}}}}"
            )
        case _:
            return AnkiTemplate(
                name=humanize_col_name(col),
                qfmt=f"{{{{bezokolicznik}}}}\n({{{{{humanize_col_name(col)}}}}})",
                afmt=f"{{{{FrontSide}}}}<hr id=\"answer\">{{{{{col}}}}}"
            )


templates = [
    _make_template(col)
    for col in filter(
        lambda name: name not in {"en", "pl"},
        VerbForms.get_cols(),
    )
]
