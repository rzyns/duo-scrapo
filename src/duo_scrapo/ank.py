from pathlib import Path
from typing import Literal, NotRequired, TypedDict, cast

import anki
import anki.collection
import anki.decks
import anki.errors
import anki.hooks
import anki.models
import anki.notes

from attr import asdict
from attrs import define
from pydantic import ConfigDict, TypeAdapter, with_config
from rich import print  # noqa: A004

# import duo_scrapo.templates.czasowniki
from duo_scrapo.Morf import VerbForms
from duo_scrapo.templates import AnkiTemplate, dedent
import duo_scrapo.templates.czasowniki
import duo_scrapo.templates.rzeczowniki
from duo_scrapo.export import export_czasowniki, export_rzeczowniki
from duo_scrapo.words.nouns import NounForms
from duo_scrapo.words.vocab import load_vocabulary
import genanki
import genanki.card
import genanki.deck
import genanki.model
import genanki.note
import genanki.util


DECK_ID = 2103513676
MODEL_ID_CZASOWNIKI = 2057651084
MODEL_ID_RZECZOWNIKI = 2026523460


class ModelAlreadyExistsError(Exception):
    def __init__(self, message: str = "Model already exists"):
        self.message = message
        super().__init__(self.message)


_model_config = ConfigDict(extra="allow")


@with_config(config=_model_config)
class Template(TypedDict):
    name: str
    ord: NotRequired[int | None]
    qfmt: str
    afmt: str
    bqfmt: str | None
    bafmt: str | None
    did: int | None
    bfont: str | None
    bsize: int | None
    id: int | None
    styling: NotRequired[str | None]


TemplateTA = TypeAdapter(Template)


def to_template(obj: anki.models.TemplateDict) -> Template:
    TemplateTA.validate_python(obj)
    return cast(Template, obj)


def from_template(obj: Template) -> anki.models.TemplateDict:
    TemplateTA.validate_python(obj)
    return cast(anki.models.TemplateDict, obj)


@with_config(config=_model_config)
class Field(TypedDict):
    name: str
    ord: NotRequired[int | None]
    sticky: bool
    rtl: bool
    font: str
    size: int
    description: str
    plainText: bool
    collapsed: bool
    excludedFromSearch: NotRequired[bool]
    id: int | None
    tag: None
    preventDeletion: bool


FieldTA = TypeAdapter(Field)


def to_field(obj: anki.models.FieldDict) -> Field:
    FieldTA.validate_python(obj)
    return cast(Field, obj)


def from_field(obj: Field) -> anki.models.FieldDict:
    FieldTA.validate_python(obj)
    return cast(anki.models.FieldDict, obj)


@with_config(config=_model_config)
class Model(TypedDict):
    id: int
    name: str
    type: int
    mod: int
    usn: int
    sortf: int
    did: int | None
    tmpls: list[Template]
    flds: list[Field]
    css: str
    req: list[tuple[int, str, tuple[int]]]


ModelTA = TypeAdapter(Model)


def to_model(obj: anki.models.NotetypeDict) -> Model:
    ModelTA.validate_python(obj)
    return cast(Model, obj)


def from_model(obj: Model) -> anki.models.NotetypeDict:
    return cast(anki.models.NotetypeDict, obj)


def add_fields_to_note_type(col: anki.collection.Collection, note_type: Model, fields: tuple[str, ...]) -> Model:
    model = col.models.by_name(note_type["name"])
    model = note_type if model is None else to_model(model)

    for field_name in fields:
        field = col.models.new_field(field_name)
        col.models.add_field(from_model(model), field)

    return model


def add_template(col: anki.collection.Collection, note_type: Model, tpl: AnkiTemplate) -> Model:
    for existing_template in note_type['tmpls']:
        if existing_template['name'] == tpl.name:
            for k, a in asdict(tpl).items():
                existing_template[k] = a

            return note_type

    new_tpl = col.models.new_template(tpl.name)
    template = to_template(new_tpl)

    for k, a in asdict(tpl).items():
        template[k] = a

    note_type['tmpls'].append(template)

    return note_type


def add_note_to_collection(col: anki.collection.Collection, note_type: Model, note: dict[str, str]) -> anki.notes.Note:
    # Generated by Copilot
    """
    Adds notes to the given Collection.

    Parameters:
    col (anki.collection.Collection): The Anki collection.
    note_type (anki.models.NoteType): The NoteType to which the notes will be added.
    notes (Iterable[anki.notes.Note]): An iterable of notes to add to the Collection.
    """
    new_note = col.new_note(notetype=from_model(note_type))
    for field_name, field_value in note.items():
        new_note[field_name] = field_value

    # deck_id = col.default_deck_for_notetype(anki.models.NotetypeId(note_type["id"]))
    deck_id = anki.decks.DeckId(DECK_ID)
    try:
        col.update_note(new_note)
    except anki.errors.NotFoundError:
        col.add_note(new_note, deck_id=deck_id)  # , deck_id=anki.decks.DeckId(0))

    return new_note


def add_czasowniki_to_collection(col: anki.collection.Collection, collection_name: Literal["czasowniki"] = "czasowniki"):
    # Sprawdź, czy typ notatki "Czasowniki" już istnieje
    czasowniki = col.models.by_name(collection_name.capitalize())

    if czasowniki is None:
        # Utwórz nowy typ notatki
        czasowniki = col.models.new("Czasowniki")

    czasowniki = to_model(czasowniki)
    czasowniki["id"] = MODEL_ID_CZASOWNIKI

    # Dodaj pola do typu notatki
    # add_fields_to_note_type(col, new_note_type, ("Front", "Back", "pl", "en"))
    add_fields_to_note_type(col, czasowniki, ("pl", "en"))
    add_fields_to_note_type(col, czasowniki, VerbForms.get_cols())

    seen: list[str] = []
    # Dodaj szablon do typu notatki
    for tpl in duo_scrapo.templates.czasowniki.templates:
        add_template(col, czasowniki, tpl)
        seen.append(tpl.qfmt)

    # if czasowniki["id"]:
    col.models.update_dict(from_model(czasowniki))
    # else:
    # col.models.add_dict(from_model(czasowniki))
    # try:
    #     # Dodaj nowy typ notatki do kolekcji
    #     col.models.add(from_model(czasowniki))
    # except anki.errors.CardTypeError:
    #     print(dict(enumerate(duo_scrapo.templates.czasowniki.templates)))
    #     raise

    vocab = load_vocabulary()
    for (word, forms) in export_czasowniki(vocab):
        # Utwórz nową notatkę
        add_note_to_collection(col, czasowniki, dict(
            pl=word.term,
            en=word.definition,
            **forms.as_dict(),
        ))


def add_rzeczowniki_to_collection(col: anki.collection.Collection, collection_name: Literal["rzeczowniki"]):
    # Sprawdź, czy typ notatki "Rzeczowniki" już istnieje
    rzeczowniki = col.models.by_name(collection_name.capitalize())

    if rzeczowniki is None:
        # Utwórz nowy typ notatki
        rzeczowniki = col.models.new("Rzeczowniki")

    rzeczowniki = to_model(rzeczowniki)
    rzeczowniki["id"] = MODEL_ID_RZECZOWNIKI

    # Dodaj pola do typu notatki
    add_fields_to_note_type(col, rzeczowniki, ("pl", "en"))
    add_fields_to_note_type(col, rzeczowniki, NounForms.get_cols())

    rzeczowniki["tmpls"].clear()
    # Dodaj szablon do typu notatki
    for tpl in duo_scrapo.templates.rzeczowniki.templates:
        add_template(col, rzeczowniki, tpl)

    if rzeczowniki["id"]:
        col.models.update_dict(from_model(rzeczowniki))
    else:
        # Dodaj nowy typ notatki do kolekcji
        col.models.add_dict(from_model(rzeczowniki))

    vocab = load_vocabulary()
    for (word, forms) in export_rzeczowniki(vocab):
        # Utwórz nową notatkę
        add_note_to_collection(col, rzeczowniki, dict(
            pl=word.term,
            en=word.definition,
            **forms.as_dict(),
        ))


def zmain():
    # Ścieżka do pliku kolekcji Anki
    # filepath = Path.cwd() / "dev/collection.anki2"
    # filepath = Path.cwd() / "rzyns/collection.anki2"
    filepath = Path.cwd() / "base/User 1/collection.anki2"

    # Usuń istniejący plik, jeśli istnieje
    # if filepath.exists():
    #     filepath.unlink()

    # Otwórz kolekcję Anki
    col = anki.collection.Collection(filepath.as_posix())

    @define
    class Check:
        notes: int
        cards: int
        fields: int

    def _get_counts():
        return Check(
            notes=col.note_count(),
            cards=col.card_count(),
            fields=len(col.models.all_names()),
        )

    start_count = _get_counts()
    add_czasowniki_to_collection(col)
    # col.close()

    # col = anki.collection.Collection(filepath.as_posix())
    # add_rzeczowniki_to_collection(col, "rzeczowniki")
    end_count = _get_counts()
    col.close()

    if end_count != start_count:
        print(dedent(f"""
        Notatki: {start_count.notes} -> {end_count.notes}
        Karty: {start_count.cards} -> {end_count.cards}
        Pola: {start_count.fields} -> {end_count.fields}
        """))
    else:
        print("Notatka została dodana do kolekcji Anki.")


def main():
    deck = genanki.Deck(DECK_ID, name="DuoScrapo")

    model = genanki.model.Model(
        model_id=MODEL_ID_CZASOWNIKI,
        name="Czasowniki",
        fields=[
            {"name": col}
            for col in ("en", "pl", *VerbForms.get_cols())
        ],
        templates=[
            asdict(a)
            for a in duo_scrapo.templates.czasowniki.templates
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

    deck.add_model(model)

    vocab = load_vocabulary()
    for (word, forms) in export_czasowniki(vocab):
        fields = (word.definition, word.term, *forms.to_rows())
        note = genanki.note.Note(
            model=model,
            fields=list(fields),
        )

        deck.add_note(note)

    genanki.Package(deck).write_to_file("deck.apkg")


if __name__ == "__main__":
    main()
