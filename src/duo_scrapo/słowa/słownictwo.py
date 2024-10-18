from pathlib import Path
import json

from attrs import define, field
import cattrs


@define
class TermDefinition:
    term: str = field()
    definition: str = field()


@define
class Term:
    term: str = field()
    definitions: list[TermDefinition] = field()


def load_vocabulary() -> list[TermDefinition]:
    return cattrs.structure(json.loads(Path("results.json").read_bytes()), list[TermDefinition])
