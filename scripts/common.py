from dataclasses import dataclass
from typing import Tuple, List, Set, Iterable, Optional

from dataclasses_json import dataclass_json, LetterCase

Argument = Tuple[int, int]

QUESTION_FIELDS = ['wh', 'subj', 'obj', 'aux', 'prep', 'obj2', 'is_passive', 'is_negated']

STR_FORMAT_ANSWER_SEPARATOR = "~!~"  # Separates between answers when represented as a string


class Question:
    def __init__(self, **kwargs):
        self.text = kwargs['text']
        self.wh = kwargs['wh'].lower()
        self.subj =kwargs['subj']
        self.obj = kwargs['obj']
        self.aux = kwargs['aux']
        self.prep = kwargs['prep']
        self.obj2 = kwargs['obj2']
        self.is_passive = kwargs['is_passive']
        self.is_negated = kwargs['is_negated']

    def __str__(self):
        return self.text

    def __lt__(self, other):
        return self.text < other.text

    def __hash__(self):
        return hash(self.text)

    def __eq__(self, other):
        return self.text == other.text


class Role:
    def __init__(self, question: Question, arguments: Iterable[Tuple[Argument, ...]]):
        self.question = question
        self.arguments = tuple(arguments)

    def text(self):
        return self.question.text

    def __lt__(self, other: 'Role'):
        return self.question < other.question

    def __repr__(self):
        return f"{self.text()} ==> { ' / '.join(str(a) for a in self.arguments)}"


@dataclass_json
@dataclass
class QuestionAnswer:
    """
    Adheres to the csv format in qasrl-gs
    """

    qasrl_id: str
    verb_idx: int
    verb: str
    question: str
    answer: str
    answer_range: str
    verb_form: Optional[str] = None
    wh: Optional[str] = None
    aux: Optional[str] = None
    subj: Optional[str] = None
    obj: Optional[str] = None
    prep: Optional[str] = None
    obj2: Optional[str] = None
    is_negated: Optional[bool] = None
    is_passive: Optional[bool] = None

    @staticmethod
    def answer_obj_to_str(answer_range: List[str]) -> str:
        return STR_FORMAT_ANSWER_SEPARATOR.join([x for x in answer_range])

    @staticmethod
    def answer_range_obj_to_str(answer_range: List[Argument]) -> str:
        return STR_FORMAT_ANSWER_SEPARATOR.join([f"{x[0]}:{x[1]}" for x in answer_range])
