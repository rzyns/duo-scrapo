import asyncio
from pydantic.dataclasses import dataclass
from pydantic import TypeAdapter
from anyio import Path

@dataclass
class VocabularyItem:
    word: str
    definition: str

VocabularyList = TypeAdapter(list[VocabularyItem])

async def main():
    data: list[VocabularyItem] = VocabularyList.validate_json(await Path('results.json').read_text(encoding="utf-8"))

    with open("vocabulary.tsv", "w", encoding="utf-8") as f:
        for item in data:
            f.write(f"{item.word}\t{item.definition}\n")

def run():
    asyncio.run(main())
