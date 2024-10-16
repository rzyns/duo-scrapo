import pytest
from enum import Enum, Flag, auto
from duo_scrapo import flag


class FLG(flag.Flag):
    A = "a"
    B = "b"
    C = "c"
    D = "d"

    E = frozenset({"a", "b"})


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


def test_only_allows_existing_members():
    with pytest.raises(ValueError, match="is not a valid FLG"):
        FLG("F")


def test_foo():
    assert FLG("A")
    assert FLG("A") == FLG.A

    a = FLG("A")
    b = FLG("B")
    left = a & b
    right = FLG.A & FLG.B
    result = left == right
    assert result

    assert FLG("A") | FLG("B") == FLG.A | FLG.B
    assert (FLG.A | FLG.B)._value_ == frozenset({"a", "b"})  # type: ignore[attr-defined]
    assert FLG("A") | {"b"} == FLG.A | {"b"}

    assert FLG("A") | {"b"} == FLG.A | {"b"}

    actual = FLG.A | {"b"}
    assert actual._value_ == frozenset({"a", "b"})  # type: ignore[attr-defined]
    assert {"a"} | FLG("B") == {"a"} | FLG.B

    assert FLG("A") & FLG("B") == FLG.A & FLG.B
    assert FLG("A") & {"b"} == FLG.A & {"b"}
    assert {"a"} & FLG("B") == {"a"} & FLG.B

    assert FLG("A") ^ FLG("B") == FLG.A ^ FLG.B
    assert FLG("A") ^ {"b"} == FLG.A ^ {"b"}
    assert {"a"} ^ FLG("B") == {"a"} ^ FLG.B

    assert FLG("A") - FLG("B") == FLG.A - FLG.B
