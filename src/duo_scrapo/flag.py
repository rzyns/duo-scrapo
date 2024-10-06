import enum
from typing import Any, Self, TypeGuard
from collections.abc import Set


def is_frozenset_str(obj: object) -> TypeGuard[frozenset[str]]:
    if isinstance(obj, frozenset):
        for i in obj:
            i: Any
            if not isinstance(i, str):
                return False
        return True
    return False


# class StringFlag(metaclass=enum.EnumType):
class Flag(enum.Enum):
    _value_: frozenset[str]

    @classmethod
    def _missing_(cls, value: str | frozenset[str] | object) -> Self | None:
        if isinstance(value, str):
            if value in cls.__members__:
                return cls[value]
            else:
                return None
        elif is_frozenset_str(value):
            known = frozenset({s for v in cls.__members__.values() for s in v.value})
            if value > known:
                return None
            obj = object.__new__(cls)
            obj._name_ = repr(value)
            obj._value_ = value
            return obj
        return None

    def __init__(self, value: frozenset[str] | str):
        # return frozenset(value)
        self._value_ = value if isinstance(value, frozenset) else frozenset([value])

    def __contains__(self, other: Self | Set[str]) -> bool:
        if isinstance(other, Flag):
            return self._value_ >= other._value_
        return self._value_ >= other

    def __eq__(self, value: object) -> bool:
        a = self._value_
        b = value._value_ if isinstance(value, Flag) else value
        return a.__eq__(b)

    def __or__(self: Self, other: Self | Set[str]):
        if isinstance(other, Flag):
            return self.__class__(self._value_ | other._value_)
        return self.__class__(self._value_ | other)

    def __ror__(self: Self, other: Self | Set[str]) -> Self:
        return self.__or__(other)

    def __and__(self, other: Self | Set[str]) -> Self:
        if isinstance(other, Flag):
            return self.__class__(self._value_ & other._value_)
        return self.__class__(self._value_ & other)

    def __rand__(self, other: Self | Set[str]) -> Self:
        return self.__and__(other)

    def __xor__(self, other: Self | Set[str]) -> Self:
        if isinstance(other, Flag):
            return self.__class__(self._value_ ^ other._value_)
        return self.__class__(self._value_ ^ other)

    def __rxor__(self, other: Self | Set[str]) -> Self:
        return self.__xor__(other)

    def __sub__(self, other: Self | Set[str]) -> Self:
        if isinstance(other, Flag):
            return self.__class__(self._value_ - other._value_)
        return self.__class__(self._value_ - other)

    def __add__(self, other: Self | Set[str]) -> Self:
        return NotImplemented

    def __ge__(self, other: Self | Set[str]) -> bool:
        if isinstance(other, Flag):
            return self._value_ >= other._value_
        return self._value_ >= other

    def __gt__(self, other: Self | Set[str]) -> bool:
        if isinstance(other, Flag):
            return self._value_ > other._value_
        return self._value_ > other

    def __lt__(self, other: Self | Set[str]) -> bool:
        if isinstance(other, Flag):
            return self._value_ < other._value_
        return self._value_ < other

    def __le__(self, other: Self | Set[str]) -> bool:
        if isinstance(other, Flag):
            return self._value_ <= other._value_
        return self._value_ <= other

    def __str__(self) -> str:
        if len(self._value_) == 1:
            return next(iter(self._value_))
        return ".".join(reversed(list(self._value_)))

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}.{self._name_}: '{self.__str__()}'>"
