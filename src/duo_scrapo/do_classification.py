from pathlib import Path
import json

import cattrs

from duo_scrapo.words.vocab import TermDefinition

from .Morf import Morf, Word


def do_classification():
    m = Morf()
    data = cattrs.structure(
        json.loads(Path("results.json").read_bytes()),
        list[TermDefinition],
    )

    seen: list[str] = []
    roots: list[tuple[Word, TermDefinition]] = []
    for datum in data:
        analysis = m.analyze(datum.term)

        for item in analysis:
            if item.lemma.word not in seen:
                roots.append((item, datum))
                # seen.append(item.lemma.word)

    with open("out.csv", "w", encoding="utf-8") as f:
        for (root, vocabItem) in roots:
            print(f"{vocabItem.term} (Root: {root.lemma}) => {vocabItem.definition}")
            f.write(f"{vocabItem.term}\t{root.lemma}\t{vocabItem.definition}\n")

        # forms = m.generate(root.lemma.word)
        # for form in forms:
        #     print(form)

        # print()
