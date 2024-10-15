from _typeshed import Incomplete
from collections.abc import Iterable
from typing import Final, Literal, NoReturn

class _SwigNonDynamicMeta(type):
    __setattr__: Incomplete

CONTINUOUS_NUMBERING: Final = 202
CONDITIONALLY_CASE_SENSITIVE: Final = 100
SKIP_WHITESPACES: Final = 301
ANALYSE_ONLY: Final = 401
GENERATE_ONLY: Final = 402
BOTH_ANALYSE_AND_GENERATE: Final = 403
__version__: Final = '1.99.9'
GENDERS: tuple[Literal['m1'], Literal['m2'], Literal['m3'], Literal['f'], Literal['n']]

type Data = tuple[str, str, str, list[str], list[str]]
type Interp = tuple[int, int, Data] | tuple[Data]

class Morfeusz:
    expand_dag: bool
    expand_tags: bool
    expand_dot: bool
    expand_underscore: bool

    def __init__(
        self,
        dict_name: str | None = None,
        dict_path: str | None = None,
        analyse: bool = True,
        generate: bool = True,
        expand_dag: bool = False,
        expand_tags: bool = False,
        expand_dot: bool = True,
        expand_underscore: bool = True,
        aggl: str | None = None,
        praet: str | None = None,
        separate_numbering: bool = True,
        case_handling: Literal[100, 101, 102] = 100,
        whitespace: Literal[301, 302, 303] = 301
    ) -> None: ...

    def add_dictionary_path(self, dict_path: str) -> None: ...
    def analyse(self, text: str) -> Iterable[Interp]: ...
    def generate(self, lemma: str, tag_id: str | None = None) -> list[tuple[str, str, str, list[NoReturn], list[NoReturn]]]: ...
    def dict_id(self) -> str: ...
    def dict_copyright(self) -> str: ...

class SwigPyIterator:
    thisown: SwigPyIterator
    def __init__(self, *args, **kwargs) -> None: ...
    __swig_destroy__: Incomplete
    def value(self): ...
    def incr(self, n: int = 1): ...
    def decr(self, n: int = 1): ...
    def distance(self, x): ...
    def equal(self, x): ...
    def copy(self): ...
    def next(self): ...
    def __next__(self): ...
    def previous(self): ...
    def advance(self, n): ...
    def __eq__(self, x): ...
    def __ne__(self, x): ...
    def __iadd__(self, n): ...
    def __isub__(self, n): ...
    def __add__(self, n): ...
    def __sub__(self, *args): ...
    def __iter__(self): ...

class InterpsList:
    thisown: Incomplete
    def iterator(self): ...
    def __iter__(self): ...
    def __nonzero__(self): ...
    def __bool__(self) -> bool: ...
    def __len__(self) -> int: ...
    def __getslice__(self, i, j): ...
    def __setslice__(self, *args): ...
    def __delslice__(self, i, j): ...
    def __delitem__(self, *args) -> None: ...
    def __getitem__(self, *args): ...
    def __setitem__(self, *args) -> None: ...
    def pop(self): ...
    def append(self, x): ...
    def empty(self): ...
    def size(self): ...
    def swap(self, v): ...
    def begin(self): ...
    def end(self): ...
    def rbegin(self): ...
    def rend(self): ...
    def clear(self): ...
    def get_allocator(self): ...
    def pop_back(self): ...
    def erase(self, *args): ...
    def __init__(self, *args) -> None: ...
    def push_back(self, x): ...
    def front(self): ...
    def back(self): ...
    def assign(self, n, x): ...
    def resize(self, *args): ...
    def insert(self, *args): ...
    def reserve(self, n): ...
    def capacity(self): ...
    __swig_destroy__: Incomplete

class StringsList:
    thisown: Incomplete
    def iterator(self): ...
    def __iter__(self): ...
    def __nonzero__(self): ...
    def __bool__(self) -> bool: ...
    def __len__(self) -> int: ...
    def __getslice__(self, i, j): ...
    def __setslice__(self, *args): ...
    def __delslice__(self, i, j): ...
    def __delitem__(self, *args) -> None: ...
    def __getitem__(self, *args): ...
    def __setitem__(self, *args) -> None: ...
    def pop(self): ...
    def append(self, x): ...
    def empty(self): ...
    def size(self): ...
    def swap(self, v): ...
    def begin(self): ...
    def end(self): ...
    def rbegin(self): ...
    def rend(self): ...
    def clear(self): ...
    def get_allocator(self): ...
    def pop_back(self): ...
    def erase(self, *args): ...
    def __init__(self, *args) -> None: ...
    def push_back(self, x): ...
    def front(self): ...
    def back(self): ...
    def assign(self, n, x): ...
    def resize(self, *args): ...
    def insert(self, *args): ...
    def reserve(self, n): ...
    def capacity(self): ...
    __swig_destroy__: Incomplete

class StringsLinkedList:
    thisown: Incomplete
    def iterator(self): ...
    def __iter__(self): ...
    def __nonzero__(self): ...
    def __bool__(self) -> bool: ...
    def __len__(self) -> int: ...
    def __getslice__(self, i, j): ...
    def __setslice__(self, *args): ...
    def __delslice__(self, i, j): ...
    def __delitem__(self, *args) -> None: ...
    def __getitem__(self, *args): ...
    def __setitem__(self, *args) -> None: ...
    def pop(self): ...
    def append(self, x): ...
    def empty(self): ...
    def size(self): ...
    def swap(self, v): ...
    def begin(self): ...
    def end(self): ...
    def rbegin(self): ...
    def rend(self): ...
    def clear(self): ...
    def get_allocator(self): ...
    def pop_back(self): ...
    def erase(self, *args): ...
    def __init__(self, *args) -> None: ...
    def push_back(self, x): ...
    def front(self): ...
    def back(self): ...
    def assign(self, n, x): ...
    def resize(self, *args): ...
    def insert(self, *args): ...
    def pop_front(self): ...
    def push_front(self, x): ...
    def reverse(self): ...
    __swig_destroy__: Incomplete

class StringsSet:
    thisown: Incomplete
    def iterator(self): ...
    def __iter__(self): ...
    def __nonzero__(self): ...
    def __bool__(self) -> bool: ...
    def __len__(self) -> int: ...
    def append(self, x): ...
    def __contains__(self, x) -> bool: ...
    def __getitem__(self, i): ...
    def add(self, x): ...
    def discard(self, x): ...
    def __init__(self, *args) -> None: ...
    def empty(self): ...
    def size(self): ...
    def clear(self): ...
    def swap(self, v): ...
    def count(self, x): ...
    def begin(self): ...
    def end(self): ...
    def rbegin(self): ...
    def rend(self): ...
    def erase(self, *args): ...
    def find(self, x): ...
    def lower_bound(self, x): ...
    def upper_bound(self, x): ...
    def equal_range(self, x): ...
    def insert(self, /, __x): ...
    __swig_destroy__: Incomplete

SEPARATE_NUMBERING: Literal[201]
STRICTLY_CASE_SENSITIVE: Literal[101]
IGNORE_CASE: Literal[102]
APPEND_WHITESPACES: Literal[302]
KEEP_WHITESPACES: Literal[303]

class _Morfeusz:
    thisown: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...
    @staticmethod
    def getVersion(): ...
    @staticmethod
    def getDefaultDictName(): ...
    @staticmethod
    def getCopyright(): ...
    @staticmethod
    def createInstance(*args): ...
    def getDictID(self): ...
    def getDictCopyright(self): ...
    def clone(self): ...
    __swig_destroy__: Incomplete
    def analyse(self, text): ...
    def generate(self, lemma, tagId: Incomplete | None = None): ...
    def setAggl(self, optionString) -> None: ...
    def getAggl(self): ...
    def setPraet(self, optionString) -> None: ...
    def getPraet(self): ...
    def setCaseHandling(self, option) -> None: ...
    def getCaseHandling(self): ...
    def setTokenNumbering(self, option) -> None: ...
    def getTokenNumbering(self): ...
    def setWhitespaceHandling(self, option) -> None: ...
    def getWhitespaceHandling(self): ...
    def getIdResolver(self): ...
    def setDictionary(self, dictName) -> None: ...
    dictionarySearchPaths: Incomplete
    def getAvailableAgglOptions(self): ...
    def getAvailablePraetOptions(self): ...
    def analyse_iter(self, text): ...

cvar: Incomplete

class ResultsIterator:
    thisown: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...
    def hasNext(self): ...
    def peek(self): ...
    def next(self): ...
    __swig_destroy__: Incomplete
    def __iter__(self): ...

class IdResolver:
    thisown: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...
    def getTagsetId(self): ...
    def getTag(self, tagId): ...
    def getTagId(self, tag): ...
    def getName(self, nameId): ...
    def getNameId(self, name): ...
    def getLabelsAsUnicode(self, labelsId): ...
    def getLabels(self, labelsId): ...
    def getLabelsId(self, labelsStr): ...
    def getTagsCount(self): ...
    def getNamesCount(self): ...
    def getLabelsCount(self): ...
    __swig_destroy__: Incomplete

class MorphInterpretation:
    thisown: Incomplete
    def __init__(self) -> None: ...
    @staticmethod
    def createIgn(startNode, endNode, orth, lemma): ...
    @staticmethod
    def createWhitespace(startNode, endNode, orth): ...
    def isIgn(self): ...
    def isWhitespace(self): ...
    def getTag(self, morfeusz): ...
    def getName(self, morfeusz): ...
    def getLabelsAsUnicode(self, morfeusz): ...
    def getLabels(self, morfeusz): ...
    startNode: Incomplete
    endNode: Incomplete
    tagId: Incomplete
    nameId: Incomplete
    labelsId: Incomplete
    @property
    def orth(self): ...
    @orth.setter
    def orth(self, val) -> None: ...
    @property
    def lemma(self): ...
    @lemma.setter
    def lemma(self, val) -> None: ...
    __swig_destroy__: Incomplete
