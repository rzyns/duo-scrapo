from attrs import define, field


@define
class AnkiTemplate:
    name: str = field()
    qfmt: str = field(default="")
    afmt: str = field(default="")
    styling: str | None = field(default=None)
