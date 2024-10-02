import enum
from enum import Enum, Flag, auto
from duo_scrapo import flag as _


class FLG(_.Flag):
    A = frozenset({"a"})
    B = frozenset({"b"})
    C = frozenset({"c"})
    D = frozenset({"d"})

    E = A | B


class BBB(_.Flag):
    A = "a"
    B = "b"

    @enum.member
    def C(self):
        return self.A | self.B


class StrEnum(Enum):
    A = "a"
    B = "b"
    C = "c"


class FlagEnum(Flag):
    A = auto()
    B = auto()
    C = auto()


def test_StrFlag():
    a = list(StrEnum)
    assert a == [StrEnum.A, StrEnum.B, StrEnum.C]


def test_FlagEnum():
    a = list(FlagEnum)
    assert a == [FlagEnum.A, FlagEnum.B, FlagEnum.C]

    or_ed = FlagEnum.A | FlagEnum.B
    assert or_ed.value == FlagEnum.A.value | FlagEnum.B.value


def test_FLG():
    assert FLG.__or__(FLG.A, FLG.B)  # noqa: PLC2801
    assert (FLG.A | FLG.B).__contains__(FLG.A)  # noqa: PLC2801
    assert bool(FLG)

    assert repr(FLG.A) == "<FLG.A: 'a'>"
    assert repr(FLG.E) in {"<FLG.E: 'a.b'>", "<FLG.E: 'b.a'>"}

    assert len(FLG) == 5  # noqa: PLR2004

    assert list(FLG) == [FLG.A, FLG.B, FLG.C, FLG.D, FLG.E]

    assert FLG.A in FLG.E
    assert FLG.E > FLG.B

    assert str(FLG.A) == "a"
    assert str(FLG.E) in {"a.b", "b.a"}


def test_foo():
    a = FLG("A")
    assert a
