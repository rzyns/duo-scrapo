import morfeusz2

from .words.vocab import TermDefinition

from .Morf import Morf, Word


def parse_classified_tsv():
    m = Morf()

    words: list[tuple[TermDefinition, Word]] = []

    with open("out.csv", encoding="utf-8") as f:
        for line in f:
            (vocab_word, vocab_lemma, vocab_definition) = line.strip().split("\t")
            result = list(m.analyze(vocab_lemma))
            print(f"{vocab_word} ({vocab_lemma}) => {vocab_definition}")

            for item in result:
                if item.lemma.matches(vocab_lemma):
                    words.append((TermDefinition(term=vocab_word, definition=vocab_definition), item))

    mm = morfeusz2.Morfeusz()
    with open("out2.csv", "w", encoding="utf-8") as f:
        for (vocab_word, word) in words:
            # if "inf" in word.tags:
            #     forms = [f"{f.word}:{"_".join(f.tags)}" for f in m.generate(word.lemma.word)]
            analysis = mm.analyse(word.word)
            f.write(f"{vocab_word.term}\t{word.lemma}\t{vocab_word.definition}\t{analysis}\n")
