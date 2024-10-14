from typing import Protocol

class SupportsStr(Protocol):
    def __str__(self) -> str: ...

BASE91_TABLE = list[str]
def guid_for(*values: tuple[SupportsStr]) -> str: ...
