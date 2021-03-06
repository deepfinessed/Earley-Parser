from typing import Any, Generator, Iterable, Optional, Tuple


class Token:
    """
    A token for our parser

    Attributes:
        type            The type of our token - ex. Noun
        value           The value of our token - ex. tiger
        is_constituent  If this is a constituent token - this is only set by Parser
        is_terminal     If this is a terminal token - this is only set by Parser

    Tokens can either be pre-tagged with a type, which will then be used by Parser, or have type None, in which
    case the Parser will try to infer their type based on their value and its terminal ruleset.
    """
    token_type: str
    value: Optional[str]

    def __init__(self, token_type: str, value: Optional[str]=None):
        self.token_type = token_type
        self.value = value

    def is_terminal(self) -> bool:
        return self.token_type == '_TERMINAL'

    def __str__(self) -> str:
        if self.token_type == "_TERMINAL":
            return f'"{self.value}"'
        if self.value:
            return self.value
        return self.token_type

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        if self.token_type == '_TERMINAL':
            return other.token_type == self.token_type and self.value == other.value
        return other.token_type == self.token_type

    def __hash__(self) -> int:
        if self.token_type == '_TERMINAL':
            return hash(self.value)
        return hash(self.token_type)


class Rule:
    """
    A rule for our Earley Parser

    Attributes:
        lhs             The left hand side of the rule, such as S in S -> NP VP
        rhs             The right hand side of the rule as a List, such as [NP, VP] in the above
        start_index     The index of the start of the match for the current token
        current_index   The current index of the parser - the location of the 'dot'
    """
    lhs: Token
    rhs: Tuple[Token, ...]
    start_index: int
    current_index: int
    dot_index: int
    index: Optional[Tuple[int, int]]
    previous_rule: Optional[Tuple[int, int]]
    updated_rule: Optional[Tuple[int, int]]


    def __init__(self, lhs: Token, rhs: Iterable[Token], start_index: int=0, current_index: int=0, dot_index: int=0,
                 index: Optional[Tuple[int, int]]=None, previous_rule: Optional[Tuple[int, int]]=None,
                 updated_rule: Optional[Tuple[int, int]]=None):
        self.lhs = lhs
        self.rhs = tuple(rhs)
        self.start_index = start_index
        self.current_index = current_index
        self.dot_index = dot_index
        self.index = index
        self.previous_rule = previous_rule
        self.updated_rule = updated_rule

    def get_current_token(self) -> Optional[Token]:
        try:
            return self.rhs[self.dot_index]
        except IndexError:
            return None

    def get_previous_token(self) -> Optional[Token]:
        if self.current_index < 1:
            return None
        return self.rhs[self.dot_index - 1]

    def is_completed(self) -> bool:
        return self.dot_index == len(self.rhs)

    def __str__(self) -> str:
        rhs_str = ' '.join(
            ['???' + str(item) if index == self.dot_index else str(item) for index, item in enumerate(self.rhs)]
        )
        if self.dot_index == len(self.rhs):
            rhs_str += '???'
        if not self.previous_rule:
            suffix = "scan"
        elif self.updated_rule:
            suffix = f"{outline_form(self.previous_rule)}/{outline_form(self.updated_rule)}"
        else:
            suffix = f"from {outline_form(self.previous_rule)}"
        return f'{outline_form(self.index):3} {str(self.lhs):10} ??? {rhs_str:20} [{self.start_index:2}, {self.current_index:2}] {suffix}'

    def __eq__(self, other: Any) -> bool:
        # exclusion of previous rules for equality prevents duplicate rules and infinite loops
        return isinstance(other, self.__class__) and self.lhs == other.lhs and self.rhs == other.rhs \
               and self.start_index == other.start_index and self.current_index == other.current_index \
               and self.dot_index == other.dot_index

    def __hash__(self) -> int:
        # exclusion of previous rules for equality prevents duplicate rules and infinite loops
        return hash((self.lhs, self.rhs, self.start_index, self.current_index, self.dot_index))


def _base_n(number: int, base: int) -> Generator[int, None, None]:
    if number < base:
        yield number
    else:
        number, remainder = divmod(number, base)
        yield from _base_n(number, base)
        yield remainder

def outline_form(index: Optional[Tuple[int, int]]) -> str:
    if index is None:
        return ''
    row_number, column_number = index
    suffix = ''.join(chr(ord('a') + digit) for digit in _base_n(column_number, 26))
    return f'{row_number}.{suffix}'

