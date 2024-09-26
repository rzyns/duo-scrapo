import enum
from typing import Self


# class StringFlag(metaclass=enum.EnumType):
class StringFlag(enum.Enum):
    def __init__(self, value: frozenset[str] | str):
        # return frozenset(value)
        self._value_ = value if isinstance(value, frozenset) else frozenset([value])

    def __contains__(self, other: Self) -> bool:
        return (self._value_ >= other._value_)

    def __or__(self: Self, other: Self) -> Self:
        return type(self)(self._value_ | other._value_)

    def __and__(self, other: Self) -> Self:
        return self.__class__(self._value_ & other._value_)

    def __xor__(self, other: Self) -> Self:
        return self.__class__(self._value_ ^ other._value_)

    def __sub__(self, other: Self) -> Self:
        return self.__class__(self._value_ - other._value_)

    def __add__(self, other: Self) -> Self:
        return NotImplemented

    def __ge__(self, other: Self) -> bool:
        return self._value_ >= other._value_

    def __gt__(self, other: Self) -> bool:
        return self._value_ > other._value_

    def __lt__(self, other: Self) -> bool:
        return self._value_ < other._value_

    def __le__(self, other: Self) -> bool:
        return self._value_ <= other._value_

    def __str__(self) -> str:
        if len(self._value_) == 1:
            return next(iter(self._value_))
        return ".".join(reversed(list(self._value_)))

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}.{self._name_}: '{self.__str__()}'>"
