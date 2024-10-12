from pathlib import Path
import json

import cattrs
from morfeusz2 import Morfeusz

from duo_scrapo.words.vocab import TermDefinition


def run_stuff():
    pass


def run_morfeusz_c_module():
    data = cattrs.structure(json.loads(Path("results.json").read_bytes()), list[TermDefinition])

    morfeusz = Morfeusz()

    lemma_tags: list[str] = []

    for vocab_word in data:
        analysis = morfeusz.analyse(vocab_word.term)
        for interp in analysis:
            match interp:
                case (_start, _end, (surface, lemma, tags, additional_info, annotations)):
                    pass
                case ((surface, lemma, tags, additional_info, annotations),):
                    pass
            if ":" in lemma:
                (_, t) = lemma.split(":")
                if t and t not in lemma_tags:
                    lemma_tags.append(t)
                print(f"Word: {surface}")
                print(f"Lemma: {lemma}")
                print(f"Tags: {tags}")
                print(f"Additional Info: {additional_info}")
                print(f"Annotations: {annotations}")

                print("[")
                for b in analysis:
                    print(f"\t{b},")
                print("]")

    print(lemma_tags)
