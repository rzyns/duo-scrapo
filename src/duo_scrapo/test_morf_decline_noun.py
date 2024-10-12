from .Morf import Morf
from .tag import Tag


def test_morf_conjugate_osiągnąć():
    result = Morf().conjugate_verb("osiągnąć")

    assert result is not None

    assert result.aspekt == Tag.PERFECTIVE
    assert result.bezokolicznik == "osiągnąć"

    rows = result.to_rows()
    assert rows.bezokolicznik == "osiągnąć"


def test_morf_conjugate_chodzić():
    # export_czasowniki()
    result = Morf().conjugate_verb("chodzić")

    assert result is not None

    assert result.aspekt == Tag.IMPERFECTIVE

    assert result.bezokolicznik == "chodzić"
    assert result.czas_teraźniejszy.liczba_pojedyncza.pierwsza_osoba == "chodzę"
    assert result.czas_teraźniejszy.liczba_pojedyncza.druga_osoba == "chodzisz"
    assert result.czas_teraźniejszy.liczba_pojedyncza.trzecia_osoba == "chodzi"
    assert result.czas_teraźniejszy.liczba_mnoga.pierwsza_osoba == "chodzimy"
    assert result.czas_teraźniejszy.liczba_mnoga.druga_osoba == "chodzicie"
    assert result.czas_teraźniejszy.liczba_mnoga.trzecia_osoba == "chodzą"

    assert result.rdzeń_czasu_przeszłego.liczba_pojedyncza.m1 == "chodził"
    assert result.rdzeń_czasu_przeszłego.liczba_pojedyncza.m2 == "chodził"
    assert result.rdzeń_czasu_przeszłego.liczba_pojedyncza.m3 == "chodził"
    assert result.rdzeń_czasu_przeszłego.liczba_pojedyncza.f == "chodziła"
    assert result.rdzeń_czasu_przeszłego.liczba_pojedyncza.n == "chodziło"

    assert result.rdzeń_czasu_przeszłego.liczba_mnoga.m1 == "chodzili"
    assert result.rdzeń_czasu_przeszłego.liczba_mnoga.reszta == "chodziły"

    assert result.czas_przeszły.liczba_pojedyncza.pierwsza_osoba.m1 == "chodziłem"
    assert result.czas_przeszły.liczba_pojedyncza.pierwsza_osoba.m2 == "chodziłem"
    assert result.czas_przeszły.liczba_pojedyncza.pierwsza_osoba.m3 == "chodziłem"
    assert result.czas_przeszły.liczba_pojedyncza.pierwsza_osoba.f == "chodziłam"
    assert result.czas_przeszły.liczba_pojedyncza.pierwsza_osoba.n == "chodziłom"

    assert result.czas_przeszły.liczba_pojedyncza.druga_osoba.m1 == "chodziłeś"
    assert result.czas_przeszły.liczba_pojedyncza.druga_osoba.m2 == "chodziłeś"
    assert result.czas_przeszły.liczba_pojedyncza.druga_osoba.m3 == "chodziłeś"
    assert result.czas_przeszły.liczba_pojedyncza.druga_osoba.f == "chodziłaś"
    assert result.czas_przeszły.liczba_pojedyncza.druga_osoba.n == "chodziłoś"

    assert result.czas_przeszły.liczba_pojedyncza.trzecia_osoba.m1 == "chodził"
    assert result.czas_przeszły.liczba_pojedyncza.trzecia_osoba.m2 == "chodził"
    assert result.czas_przeszły.liczba_pojedyncza.trzecia_osoba.m3 == "chodził"
    assert result.czas_przeszły.liczba_pojedyncza.trzecia_osoba.f == "chodziła"
    assert result.czas_przeszły.liczba_pojedyncza.trzecia_osoba.n == "chodziło"

    assert result.czas_przeszły.liczba_mnoga.pierwsza_osoba.m1 == "chodziliśmy"
    assert result.czas_przeszły.liczba_mnoga.pierwsza_osoba.reszta == "chodziłyśmy"

    assert result.czas_przeszły.liczba_mnoga.druga_osoba.m1 == "chodziliście"
    assert result.czas_przeszły.liczba_mnoga.druga_osoba.reszta == "chodziłyście"

    assert result.czas_przeszły.liczba_mnoga.trzecia_osoba.m1 == "chodzili"
    assert result.czas_przeszły.liczba_mnoga.trzecia_osoba.reszta == "chodziły"

    # result = Morf().decline_noun(Word(
    #     word="chodzenie",
    #     lemma=Lemma("chodzenie", tags=""),
    #     tags="subst:sg:nom:n",
    # ))

    # assert result.liczba_pojedyncza.mianownik == "chodzenie"
