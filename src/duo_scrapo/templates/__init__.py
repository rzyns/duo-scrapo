import attrs


@attrs.define
class AnkiTemplate:
    name: str = attrs.field()
    question: str = attrs.field()
    answer: str = attrs.field()
    css: str = attrs.field(default="")
