import enum
from duo_scrapo.str_flag import StringFlag


class BaseTag(StringFlag):
    pass
    # name: str

    # def __repr__(self) -> str:
    #     return self.name


class Tag(StringFlag):
    ADJECTIVE = "adj"
    INFINITIVE = "inf"
    PREDICATIVE = "pred"
    FINITIVE = "fin"
    PARTICIPLE = "part"
    ADVERB = "adv"
    NOUN = "subst"
    ncol = "ncol"
    col = "col"
    GERUND = "ger"
    PARTICIPLE_PASS_ADC = "ppas"  # noqa: S105
    IMPERATIVE = "impt"
    CONJUCTION_SUBORDINATING = "comp"
    PREPOSITION = "prep"
    CONJUCTION_COORDINATING = "conj"
    PT = "pt"
    PARTICIPLE_L = "praet"
    INTERJECTION = "interj"
    SIEBIE = "siebie"
    WINIEN = "winien"
    NUMERAL = "num"
    PPRON3 = "ppron3"
    PPRON12 = "ppron12"
    DEPRECIATIVE_FORM = "depr"
    ADJECTIVE_POST_PREPOSITIONAL = "adjp"
    ABBREVIATION = "brev"
    FRAGMENT = "frag"

    SINGULAR = "sg"
    PLURAL = "pl"

    @enum.member
    def Number(self):
        return self.SINGULAR | self.PLURAL


# class Gender(BaseTag):
    MASCULINE_HUMAN = "m1"
    MASCULINE_VIRILE = "m2"
    MASCULINE_NONVIRILE = "m3"
    FEMININE = "f"
    NEUTER = "n"

    @enum.member
    def Gender(self):
        return self.MASCULINE_HUMAN | self.MASCULINE_VIRILE | self.MASCULINE_NONVIRILE | self.FEMININE | self.NEUTER


# class Case(BaseTag):
    NOMINATIVE = "nom"
    GENITIVE = "gen"
    DATIVE = "dat"
    ACCUSATIVE = "acc"
    LOCATIVE = "loc"
    INSTRUMENTAL = "inst"
    VOCATIVE = "voc"

    @enum.member
    def Case(self):
        return self.NOMINATIVE | self.GENITIVE | self.DATIVE | self.ACCUSATIVE | self.LOCATIVE | self.INSTRUMENTAL | self.VOCATIVE


# class Person(BaseTag):
    FIRST = "pri"
    SECOND = "sec"
    THIRD = "ter"

    @enum.member
    def Person(self):
        return self.FIRST | self.SECOND | self.THIRD


# class Degree(BaseTag):
    POSITIVE = "pos"
    COMPARATIVE = "com"
    SUPERLATIVE = "sup"

    @enum.member
    def Degree(self):
        return self.POSITIVE | self.COMPARATIVE | self.SUPERLATIVE


# class Aspect(BaseTag):
    IMPERFECTIVE = "imperf"
    PERFECTIVE = "perf"

    @enum.member
    def Aspect(self):
        return self.IMPERFECTIVE | self.PERFECTIVE


# class Negation(BaseTag):
    AFFIRMATIVE = "aff"
    NEGATIVE = "neg"

    @enum.member
    def Negation(self):
        return self.AFFIRMATIVE | self.NEGATIVE


# class Accentability(BaseTag):
    ACCENTED = "akc"
    NON_ACCENTED = "nakc"

    @enum.member
    def Accentability(self):
        return self.ACCENTED | self.NON_ACCENTED

# class PostPrepositional(BaseTag):
    POST_PREPOSITIONAL = "praep"
    NON_POST_PREPOSITIONAL = "npraep"

    @enum.member
    def PostPrepositional(self):
        return self.POST_PREPOSITIONAL | self.NON_POST_PREPOSITIONAL


# class Accomodation(BaseTag):
    AGREEMENT = "congr"
    GOVERNING = "rec"

    @enum.member
    def Accomodation(self):
        return self.AGREEMENT | self.GOVERNING


# class Agglutination(BaseTag):
    AGGLUTINATIVE = "agl"
    NON_AGGLUTINATIVE = "nagl"

    @enum.member
    def Agglutination(self):
        return self.AGGLUTINATIVE | self.NON_AGGLUTINATIVE


# class Vocality(BaseTag):
    VOCALIC = "wok"
    NON_VOCALIC = "nwok"

    @enum.member
    def Vocality(self):
        return self.VOCALIC | self.NON_VOCALIC


# class FullStoppedness(BaseTag):
    FULL_STOPPED = "pun"
    NON_FULL_STOPPED = "npun"

    @enum.member
    def FullStoppedness(self):
        return self.FULL_STOPPED | self.NON_FULL_STOPPED


# class Tag(BaseTag):
#     pass


# CaseTags = frozenset({
#     BaseTag.NOMINATIVE,
#     BaseTag.GENITIVE,
#     BaseTag.DATIVE,
#     BaseTag.ACCUSATIVE,
#     BaseTag.LOCATIVE,
#     BaseTag.INSTRUMENTAL,
#     BaseTag.VOCATIVE,
# })

# NumberTags = frozenset({
#     BaseTag.SINGULAR,
#     BaseTag.PLURAL,
# })

# PersonTags = frozenset({
#     frozenset({BaseTag.PRIMARY, BaseTag.SINGULAR}),
#     frozenset({BaseTag.SECONDARY, BaseTag.SINGULAR}),
#     frozenset({BaseTag.TERTIARY, BaseTag.SINGULAR}),
#     frozenset({BaseTag.PRIMARY, BaseTag.PLURAL}),
#     frozenset({BaseTag.SECONDARY, BaseTag.PLURAL}),
#     frozenset({BaseTag.TERTIARY, BaseTag.PLURAL}),
# })


class Number(BaseTag):
    SINGULAR = "sg"
    PLURAL = "pl"


class Gender(BaseTag):
    MASCULINE_HUMAN = "m1"
    MASCULINE_VIRILE = "m2"
    MASCULINE_NONVIRILE = "m3"
    FEMININE = "f"
    NEUTER = "n"


class Case(BaseTag):
    NOMINATIVE = "nom"
    GENITIVE = "gen"
    DATIVE = "dat"
    ACCUSATIVE = "acc"
    LOCATIVE = "loc"
    INSTRUMENTAL = "instr"
    VOCATIVE = "voc"


class Person(BaseTag):
    FIRST = "pri"
    SECOND = "sec"
    THIRD = "ter"


class Degree(BaseTag):
    POSITIVE = "pos"
    COMPARATIVE = "com"
    SUPERLATIVE = "sup"


class Aspect(BaseTag):
    IMPERFECTIVE = "imperf"
    PERFECTIVE = "perf"


class Negation(BaseTag):
    AFFIRMATIVE = "aff"
    NEGATIVE = "neg"


class Accentability(BaseTag):
    ACCENTED = "akc"
    NON_ACCENTED = "nakc"


class PostPrepositional(BaseTag):
    POST_PREPOSITIONAL = "praep"
    NON_POST_PREPOSITIONAL = "npraep"


class Accomodation(BaseTag):
    AGREEMENT = "congr"
    GOVERNING = "rec"


class Agglutination(BaseTag):
    AGGLUTINATIVE = "agl"
    NON_AGGLUTINATIVE = "nagl"


class Vocality(BaseTag):
    VOCALIC = "wok"
    NON_VOCALIC = "nwok"


class FullStoppedness(BaseTag):
    FULL_STOPPED = "pun"
    NON_FULL_STOPPED = "npun"


# class Tag(BaseTag):
#     pass


# CaseTags = frozenset({
#     BaseTag.NOMINATIVE,
#     BaseTag.GENITIVE,
#     BaseTag.DATIVE,
#     BaseTag.ACCUSATIVE,
#     BaseTag.LOCATIVE,
#     BaseTag.INSTRUMENTAL,
#     BaseTag.VOCATIVE,
# })

# NumberTags = frozenset({
#     BaseTag.SINGULAR,
#     BaseTag.PLURAL,
# })

# PersonTags = frozenset({
#     frozenset({BaseTag.PRIMARY, BaseTag.SINGULAR}),
#     frozenset({BaseTag.SECONDARY, BaseTag.SINGULAR}),
#     frozenset({BaseTag.TERTIARY, BaseTag.SINGULAR}),
#     frozenset({BaseTag.PRIMARY, BaseTag.PLURAL}),
#     frozenset({BaseTag.SECONDARY, BaseTag.PLURAL}),
#     frozenset({BaseTag.TERTIARY, BaseTag.PLURAL}),
# })
