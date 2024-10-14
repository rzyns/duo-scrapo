from collections.abc import Generator, Iterable

from duo_scrapo.Morf import Morf
from duo_scrapo.tag import Tag
from duo_scrapo.words.verbs import VerbForms
from duo_scrapo.words.nouns import NounForms
from duo_scrapo.words.vocab import TermDefinition, load_vocabulary


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


if __name__ == "__main__":
    data = load_vocabulary()
    m = Morf(dict_names=["sgjp"])

    export_czasowniki(data, m)
    export_rzeczowniki(data, m)
