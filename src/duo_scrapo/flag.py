import enum
from typing import Self, overload
from collections.abc import Set


# class StringFlag(metaclass=enum.EnumType):
class Flag(enum.Enum):  # noqa: PLR0904
    _value_: frozenset[str]

    @classmethod
    def _missing_(cls, value: object):
        if isinstance(value, str | frozenset):
            a = object.__new__(cls)
            cls.__init__(a, value)
            return a
        return None

    def __init__(self, value: frozenset[str] | str):
        # return frozenset(value)
        self._value_ = value if isinstance(value, frozenset) else frozenset([value])

    def __contains__(self, other: Self | Set[str]) -> bool:
        if isinstance(other, Flag):
            return self._value_ >= other._value_
        return self._value_ >= other

    @overload
    def __or__(self: Self, other: Self) -> Self: ...
    @overload
    def __or__(self: Self, other: Set[str]) -> Set[str]: ...
    def __or__(self: Self, other: Self | Set[str]) -> Self | Set[str]:
        if isinstance(other, Flag):
            return type(self)(self._value_ | other._value_)
        return type(self)(self._value_ | other)

    @overload
    def __ror__(self: Self, other: Self) -> Self: ...
    @overload
    def __ror__(self: Self, other: Set[str]) -> Set[str]: ...
    def __ror__(self: Self, other: Self | Set[str]) -> Self | Set[str]:
        return self.__or__(other)

    @overload
    def __and__(self, other: Set[str]) -> Set[str]: ...
    @overload
    def __and__(self, other: Self) -> Self: ...
    def __and__(self, other: Self | Set[str]) -> Self | Set[str]:
        if isinstance(other, Flag):
            return self.__class__(self._value_ & other._value_)
        return self._value_ & other

    @overload
    def __rand__(self, other: Set[str]) -> Set[str]: ...
    @overload
    def __rand__(self, other: Self) -> Self: ...
    def __rand__(self, other: Self | Set[str]) -> Self | Set[str]:
        return self.__and__(other)

    @overload
    def __xor__(self, other: Self) -> Self: ...
    @overload
    def __xor__(self, other: Set[str]) -> Set[str]: ...
    def __xor__(self, other: Self | Set[str]) -> Self | Set[str]:
        if isinstance(other, Flag):
            return self.__class__(self._value_ ^ other._value_)
        return self.__class__(self._value_ ^ other)

    @overload
    def __rxor__(self, other: Self) -> Self: ...
    @overload
    def __rxor__(self, other: Set[str]) -> Set[str]: ...
    def __rxor__(self, other: Self | Set[str]) -> Self | Set[str]:
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
