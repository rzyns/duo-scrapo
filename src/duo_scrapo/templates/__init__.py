import textwrap
from typing import Protocol
import attrs


@attrs.define
class AnkiTemplate:
    name: str = attrs.field()
    qfmt: str = attrs.field(default="")
    afmt: str = attrs.field(default="")


def dedent(s: str) -> str:
    return textwrap.dedent(s).lstrip()


def field(s: str) -> str:
    return "{{" + s + "}}"


def cond(s: str) -> str:
    return field(f"#{s}")


def end_cond(s: str) -> str:
    return field(f"/{s}")


def front() -> str:
    return field("FrontSide")


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


def humanize_person(person: str, number: str) -> str:
    match person:
        case "1p":
            return "1st Person"
        case "2p":
            return "2nd Person"
        case "3p":
            return "3rd Person"
        case _:
            return person.capitalize()


def humanize_gender(gender: str) -> str:
    # match gender:
    #     case "m1":
    #         return "Masculine Virile"
    #     case "m2":
    #         return "Masculine Non-Virile"
    #     case "m3":
    #         return "Masculine Inanimate"
    #     case "f":
    #         return "Feminine"
    #     case "n":
    #         return "Neuter"
    #     case "r":
    #         return "Common"
    #     case _:
    #         return gender.capitalize()
    return gender


class TemplateModule(Protocol):
    templates: list[AnkiTemplate]
