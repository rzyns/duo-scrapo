from pathlib import Path
import json
from typing import Literal, Protocol

from attrs import define, field
import cattrs
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict, TomlConfigSettingsSource

from duo_scrapo.Morf import Morf, Word
from duo_scrapo.words.vocab import TermDefinition

type Data = tuple[str, str, str, list[str], list[str]]
type Interp = tuple[int, int, Data]


@define
class Nouny(Protocol):
    number: Literal["sg", "pl"]
    gender: Literal["m1", "m2", "m3", "f", "n"]

    nom:   str
    gen:   str
    dat:   str
    acc:   str
    loc:   str
    instr: str
    voc:   str


@define
class Verby(Word):
    aspect: Literal["imperf", "perf"]
    number: Literal["sg", "pl"]
    person: Literal[1, 2, 3]
    tense: Literal["praet", "pres", "fut"]
    mood: Literal["indic", "imper", "cond", "subj"]
    voice: Literal["act", "pass"]


def generate_mówić():
    m = Morf()
    result = m.generate("mówić")

    for word in result:
        print(word)

    seen: list[str] = []
    for word in result:
        if word.lemma.word not in seen:
            seen.append(word.lemma.word)
            for generated in m.generate(word.lemma.word):
                print(generated)
            break

    print(result)


@define
class AnkiCard:
    word: Word = field()
    definition: str = field()


@define
class Noun:
    gender: Literal["m1", "m2", "m3", "f", "n"]
    number: Literal["sg", "pl"]

    nom:   Word = field()
    gen:   Word = field()
    dat:   Word = field()
    acc:   Word = field()
    loc:   Word = field()
    instr: Word = field()
    voc:   Word = field()


@define
class AnkiNounCard(AnkiCard):
    singular: Noun = field()
    plural: Noun = field()


data = cattrs.structure(json.loads(Path("results.json").read_bytes()), list[TermDefinition])
m = Morf(dict_names=["sgjp"])


class Filter(BaseModel):
    exclude: list[str] = []


class Settings(BaseSettings):
    filter: Filter = Field(default=Filter())

    model_config = SettingsConfigDict(toml_file='config.toml')

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (TomlConfigSettingsSource(settings_cls),)


config = Settings()


class StudySet:
    pass


def export():
    pass
