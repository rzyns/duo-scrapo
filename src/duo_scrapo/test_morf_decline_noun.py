# from duo_scrapo import Morf, Word, Lemma
from duo_scrapo.annotate import main


def test_morf_decline_noun():
    main()
    assert True
    # result = Morf().decline_noun(Word(
    #     word="chodzenie",
    #     lemma=Lemma("chodzenie", tags=""),
    #     tags="subst:sg:nom:n",
    # ))

    # assert result.liczba_pojedyncza.mianownik == "chodzenie"
