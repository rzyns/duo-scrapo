import genanki
import genanki.note
from duo_scrapo.ank import main


def test_note():
    def gen(start: int):
        _s = start
        yield (_s := _s + 1)

    m = genanki.model.Model()
    n = genanki.note.Note(m, [], "", [], "foo", 0)
    genanki.note._TagList()
    assert genanki.note.Note is genanki.Note
    assert n.guid == "foo"


test_note()
