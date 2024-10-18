from collections.abc import Generator, Iterable
import textwrap
from typing import Literal, Protocol
from collections.abc import Sized
from attr import field
from attrs import define
from rich import print  # noqa: A004

from duo_scrapo.Morf import Morf
from duo_scrapo.tag import Tag
from duo_scrapo.words.adjectives import AdjectiveForms
from duo_scrapo.words.adverbs import AdverbForms
from duo_scrapo.words.prepositions import PrepositionForms
from duo_scrapo.words.pronouns import PronounForms
from duo_scrapo.words.verbs import VerbForms
from duo_scrapo.words.nouns import NounForms
from duo_scrapo.words.vocab import TermDefinition, load_vocabulary


type SomeType = Literal["adj", "noun", "verb", "pronoun", "preposition", "adverb"]


type SomeForm = VerbForms | NounForms | AdjectiveForms | PronounForms | PrepositionForms | AdverbForms


def export_rzeczowniki(data: Iterable[TermDefinition], morf: Morf | None = None) -> Generator[tuple[TermDefinition, NounForms]]:
    m = morf or Morf()

    seen_words: list[str] = []

    for vocab_word in data:
        analysis = m.analyze(vocab_word.term)

        for thing in analysis:
            if thing.tags & Tag.Case and thing.lemma.word not in seen_words:
                forms = m.decline_noun(thing)
                if forms is None:
                    continue

                seen_words.append(thing.lemma.word)

                yield (vocab_word, forms)


def zexport_rzeczowniki(data: Iterable[TermDefinition], morf: Morf | None = None) -> Generator[tuple[TermDefinition, NounForms]]:
    columns = [
        "pl",
        "en",
        "rodzaj",
        "lp_mianownik",
        "lp_dopełniacz",
        "lp_celownik",
        "lp_biernik",
        "lp_narzędnik",
        "lp_miejscownik",
        "lp_wołacz",
        "lm_mianownik",
        "lm_dopełniacz",
        "lm_celownik",
        "lm_biernik",
        "lm_narzędnik",
        "lm_miejscownik",
        "lm_wołacz",
    ]

    m = morf or Morf()

    with open("rzeczowniki.tsv", "w", encoding="utf-8") as f:
        f.write("\t".join(columns) + "\n")

        seen_words: list[str] = []
        for vocab_word in data:
            analysis = m.analyze(vocab_word.term)

            for thing in analysis:
                if thing.tags & Tag.Case and thing.lemma.word not in seen_words:
                    forms = m.decline_noun(thing)
                    if forms is None:
                        continue

                    seen_words.append(thing.lemma.word)

                    yield (vocab_word, forms)
                    print(forms)

                    f.write("\t".join([
                        vocab_word.term,
                        vocab_word.definition,
                        str(forms.rodzaj),
                        forms.liczba_pojedyncza.mianownik,
                        forms.liczba_pojedyncza.dopełniacz,
                        forms.liczba_pojedyncza.celownik,
                        forms.liczba_pojedyncza.biernik,
                        forms.liczba_pojedyncza.narzędnik,
                        forms.liczba_pojedyncza.miejscownik,
                        forms.liczba_pojedyncza.wołacz,
                        forms.liczba_mnoga.mianownik,
                        forms.liczba_mnoga.dopełniacz,
                        forms.liczba_mnoga.celownik,
                        forms.liczba_mnoga.biernik,
                        forms.liczba_mnoga.narzędnik,
                        forms.liczba_mnoga.miejscownik,
                        forms.liczba_mnoga.wołacz,
                    ]) + "\n")


def export_przymiotniki():
    pass


def export_czasowniki(data: Iterable[TermDefinition], morf: Morf | None = None) -> Generator[tuple[TermDefinition, VerbForms]]:
    m = morf or Morf()

    seen_words: list[str] = []
    for vocab_word in data:
        analysis = m.analyze(vocab_word.term)

        for thing in analysis:
            if thing.tags & Tag.Aspect and thing.lemma.word not in seen_words:
                forms = m.conjugate_verb(thing)
                if forms is None:
                    continue

                yield (vocab_word, forms)

                seen_words.append(thing.lemma.word)


@define
class Stats:
    vocab_count: int
    processed: int = field(default=0)
    adjectives: int = field(default=0)
    nouns: int = field(default=0)
    pronouns: int = field(default=0)
    verbs: int = field(default=0)

    def log(self, kind: SomeType) -> None:
        self.processed += 1
        if kind == "adj":
            self.adjectives += 1
        elif kind == "noun":
            self.nouns += 1
        elif kind == "pronoun":
            self.pronouns += 1
        elif kind == "verb":
            self.verbs += 1

    @property
    def unhandled(self) -> int:
        return self.vocab_count - self.adjectives - self.nouns - self.verbs

    @property
    def unprocessed(self) -> int:
        return self.vocab_count - self.processed

    def __str__(self) -> str:
        return textwrap.dedent(f"""
            Stats:
                Processed: {self.processed}
                    Adjec:     {self.adjectives}
                    Nouns:     {self.nouns}
                    Pronouns:  {self.pronouns}
                    Verbs:     {self.verbs}
                    --------------------------------
                    Total: {self.processed}

                Unhandled: {self.unhandled}
                Unprocessed: {self.unprocessed}
            """).lstrip()


class SizedIterable[T](Sized, Iterable[T], Protocol):
    pass


def export(data: SizedIterable[TermDefinition], morf: Morf | None = None) -> Generator[tuple[TermDefinition, SomeForm, Stats]]:
    m = morf or Morf()

    seen_words: list[tuple[SomeType, str]] = []
    stats = Stats(vocab_count=len(data))

    for vocab_word in data:
        analysis = m.analyze(vocab_word.term)

        for thing in analysis:
            handled = False

            if thing.is_adj() and ("adj", thing.lemma.word) not in seen_words:
                forms = m.decline_adjective(thing)
                if forms is not None:
                    seen_words.append(("adj", thing.lemma.word))
                    handled = True
                    stats.log("adj")
                    yield (vocab_word, forms, stats)

            if thing.is_verb() and ("verb", thing.lemma.word) not in seen_words:
                forms = m.conjugate_verb(thing)
                if forms is not None:
                    seen_words.append(("verb", thing.lemma.word))
                    handled = True
                    stats.log("verb")
                    yield (vocab_word, forms, stats)

            if thing.is_noun() and ("noun", thing.lemma.word) not in seen_words:
                forms = m.decline_noun(thing)
                if forms is not None:
                    seen_words.append(("noun", thing.lemma.word))
                    handled = True
                    stats.log("noun")
                    yield (vocab_word, forms, stats)

            if thing.is_pronoun() and ("pronoun", thing.lemma.word) not in seen_words:
                forms = m.decline_pronoun(thing)
                if forms is not None:
                    seen_words.append(("pronoun", thing.lemma.word))
                    handled = True
                    stats.log("pronoun")
                    yield (vocab_word, forms, stats)

            if thing.is_preposition() and ("preposition", thing.lemma.word) not in seen_words:
                forms = m.get_preposition_supported_cases(thing)
                if forms is not None:
                    seen_words.append(("preposition", thing.lemma.word))
                    handled = True
                    stats.log("preposition")
                    yield (vocab_word, forms, stats)

            if thing.is_adv() and ("adverb", thing.lemma.word) not in seen_words:
                forms = AdverbForms(form=thing.lemma.word)
                seen_words.append(("adverb", thing.lemma.word))
                handled = True
                stats.log("adverb")
                yield (vocab_word, forms, stats)

            if not handled and thing.lemma.word not in [w for _, w in seen_words]:
                print(f"Unhandled: {vocab_word.term} => {thing.lemma} [ {thing.tags} ]")


if __name__ == "__main__":
    data = load_vocabulary()
    m = Morf(dict_names=["sgjp"])

    stats: Stats | None = None
    for _, __, stats_ in export(data, m):
        stats = stats_

    if stats is not None:
        print(str(stats))
