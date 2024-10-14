from _typeshed import SupportsNext
from sqlite3 import Cursor
from typing import Any
from genanki import Note
from genanki.model import Model

"""
This type stub file was generated by pyright.
"""

"""
This type stub file was generated by pyright.
"""

class Deck:
    deck_id: int
    notes: list[Note]

    def __init__(
        self, deck_id: int, name: str, description: str | None = None
    ) -> None: ...
    def add_note(self, note: Note) -> None: ...
    def add_model(self, model: Model) -> None: ...
    def to_json(self) -> dict[Any, Any]: ...
    def write_to_db[T](
        self, cursor: Cursor, timestamp: float, id_gen: SupportsNext[T]
    ) -> None: ...
    def write_to_file(self, file: str) -> None:
        """
        Write this deck to a .apkg file.
        """

    def write_to_collection_from_addon(self) -> None:
        """
        Write to local collection. *Only usable when running inside an Anki addon!* Only tested on Anki 2.1.

        This writes to a temporary file and then calls the code that Anki uses to import packages.

        Note: the caller may want to use mw.checkpoint and mw.reset as follows:

          # creates a menu item called "Undo Add Notes From MyAddon" after this runs
          mw.checkpoint('Add Notes From MyAddon')
          # run import
          my_package.write_to_collection_from_addon()
          # refreshes main view so new deck is visible
          mw.reset()

        Tip: if your deck has the same name and ID as an existing deck, then the notes will get placed in that deck rather
        than a new deck being created.
        """
