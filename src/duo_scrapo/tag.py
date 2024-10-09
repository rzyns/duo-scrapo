from duo_scrapo.flag import Flag


class BaseTag(Flag):
    pass
    # name: str

    # def __repr__(self) -> str:
    #     return self.name


class Tag(Flag):
    ADJECTIVE = frozenset({"adj"})
    INFINITIVE = frozenset({"inf"})
    PREDICATIVE = frozenset({"pred"})
    FINITIVE = frozenset({"fin"})
    PARTICIPLE = frozenset({"part"})
    ADVERB = frozenset({"adv"})
    NOUN = frozenset({"subst"})
    ncol = frozenset({"ncol"})
    col = frozenset({"col"})
    GERUND = frozenset({"ger"})
    PARTICIPLE_PASS_ADC = frozenset({"ppas"})
    IMPERATIVE = frozenset({"impt"})
    CONJUCTION_SUBORDINATING = frozenset({"comp"})
    PREPOSITION = frozenset({"prep"})
    CONJUCTION_COORDINATING = frozenset({"conj"})
    PT = frozenset({"pt"})
    PARTICIPLE_L = frozenset({"praet"})
    INTERJECTION = frozenset({"interj"})
    SIEBIE = frozenset({"siebie"})
    WINIEN = frozenset({"winien"})
    NUMERAL = frozenset({"num"})
    PPRON3 = frozenset({"ppron3"})
    PPRON12 = frozenset({"ppron12"})
    DEPRECIATIVE_FORM = frozenset({"depr"})
    ADJECTIVE_POST_PREPOSITIONAL = frozenset({"adjp"})
    ABBREVIATION = frozenset({"brev"})
    FRAGMENT = frozenset({"frag"})

    SINGULAR = frozenset({"sg"})
    PLURAL = frozenset({"pl"})

    Number = SINGULAR | PLURAL


# class Gender(BaseTag):
    MASCULINE_HUMAN = frozenset({"m1"})
    MASCULINE_VIRILE = frozenset({"m2"})
    MASCULINE_NONVIRILE = frozenset({"m3"})
    FEMININE = frozenset({"f"})
    NEUTER = frozenset({"n"})

    Gender = MASCULINE_HUMAN | MASCULINE_VIRILE | MASCULINE_NONVIRILE | FEMININE | NEUTER
    Masculine = MASCULINE_HUMAN | MASCULINE_VIRILE | MASCULINE_NONVIRILE


# class Case(BaseTag):
    NOMINATIVE = frozenset({"nom"})
    GENITIVE = frozenset({"gen"})
    DATIVE = frozenset({"dat"})
    ACCUSATIVE = frozenset({"acc"})
    LOCATIVE = frozenset({"loc"})
    INSTRUMENTAL = frozenset({"inst"})
    VOCATIVE = frozenset({"voc"})

    Case = NOMINATIVE | GENITIVE | DATIVE | ACCUSATIVE | LOCATIVE | INSTRUMENTAL | VOCATIVE

# class Person(BaseTag):
    FIRST = frozenset({"pri"})
    SECOND = frozenset({"sec"})
    THIRD = frozenset({"ter"})

    Person = FIRST | SECOND | THIRD


# class Degree(BaseTag):
    POSITIVE = frozenset({"pos"})
    COMPARATIVE = frozenset({"com"})
    SUPERLATIVE = frozenset({"sup"})

    Degree = POSITIVE | COMPARATIVE | SUPERLATIVE


# class Aspect(BaseTag):
    IMPERFECTIVE = frozenset({"imperf"})
    PERFECTIVE = frozenset({"perf"})

    Aspect = IMPERFECTIVE | PERFECTIVE


# class Negation(BaseTag):
    AFFIRMATIVE = frozenset({"aff"})
    NEGATIVE = frozenset({"neg"})

    Negation = AFFIRMATIVE | NEGATIVE


# class Accentability(BaseTag):
    ACCENTED = frozenset({"akc"})
    NON_ACCENTED = frozenset({"nakc"})

    Accentability = ACCENTED | NON_ACCENTED

# class PostPrepositional(BaseTag):
    POST_PREPOSITIONAL = frozenset({"praep"})
    NON_POST_PREPOSITIONAL = frozenset({"npraep"})

    PostPrepositional = POST_PREPOSITIONAL | NON_POST_PREPOSITIONAL


# class Accomodation(BaseTag):
    AGREEMENT = frozenset({"congr"})
    GOVERNING = frozenset({"rec"})

    Accomodation = AGREEMENT | GOVERNING


# class Agglutination(BaseTag):
    AGGLUTINATIVE = frozenset({"agl"})
    NON_AGGLUTINATIVE = frozenset({"nagl"})

    Agglutination = AGGLUTINATIVE | NON_AGGLUTINATIVE


# class Vocality(BaseTag):
    VOCALIC = frozenset({"wok"})
    NON_VOCALIC = frozenset({"nwok"})

    Vocality = VOCALIC | NON_VOCALIC


# class FullStoppedness(BaseTag):
    FULL_STOPPED = frozenset({"pun"})
    NON_FULL_STOPPED = frozenset({"npun"})

    FullStoppedness = FULL_STOPPED | NON_FULL_STOPPED


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
    SINGULAR = frozenset({"sg"})
    PLURAL = frozenset({"pl"})


class Gender(BaseTag):
    MASCULINE_HUMAN = frozenset({"m1"})
    MASCULINE_VIRILE = frozenset({"m2"})
    MASCULINE_NONVIRILE = frozenset({"m3"})
    FEMININE = frozenset({"f"})
    NEUTER = frozenset({"n"})


class Case(BaseTag):
    NOMINATIVE = frozenset({"nom"})
    GENITIVE = frozenset({"gen"})
    DATIVE = frozenset({"dat"})
    ACCUSATIVE = frozenset({"acc"})
    LOCATIVE = frozenset({"loc"})
    INSTRUMENTAL = frozenset({"instr"})
    VOCATIVE = frozenset({"voc"})


class Person(BaseTag):
    FIRST = frozenset({"pri"})
    SECOND = frozenset({"sec"})
    THIRD = frozenset({"ter"})


class Degree(BaseTag):
    POSITIVE = frozenset({"pos"})
    COMPARATIVE = frozenset({"com"})
    SUPERLATIVE = frozenset({"sup"})


class Aspect(BaseTag):
    IMPERFECTIVE = frozenset({"imperf"})
    PERFECTIVE = frozenset({"perf"})


class Negation(BaseTag):
    AFFIRMATIVE = frozenset({"aff"})
    NEGATIVE = frozenset({"neg"})


class Accentability(BaseTag):
    ACCENTED = frozenset({"akc"})
    NON_ACCENTED = frozenset({"nakc"})


class PostPrepositional(BaseTag):
    POST_PREPOSITIONAL = frozenset({"praep"})
    NON_POST_PREPOSITIONAL = frozenset({"npraep"})


class Accomodation(BaseTag):
    AGREEMENT = frozenset({"congr"})
    GOVERNING = frozenset({"rec"})


class Agglutination(BaseTag):
    AGGLUTINATIVE = frozenset({"agl"})
    NON_AGGLUTINATIVE = frozenset({"nagl"})


class Vocality(BaseTag):
    VOCALIC = frozenset({"wok"})
    NON_VOCALIC = frozenset({"nwok"})


class FullStoppedness(BaseTag):
    FULL_STOPPED = frozenset({"pun"})
    NON_FULL_STOPPED = frozenset({"npun"})


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
