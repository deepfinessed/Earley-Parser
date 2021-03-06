from typing import List, Dict, Set

from Rule import Token, Rule

class Parser:
    """
    An Earley parser implemented based on the algorithm in the text

    Attributes:
        rule_dict           A dictionary containing our base ruleset
        chart               The chart for our parse
        input_tokens        The string to be parsed
        current_position    The position in the parse
    """

    grammar: Dict[Token, List[Rule]]
    terminals: Dict[Token, Set[str]]
    chart: List[List[Rule]]
    input_tokens: List[Token]
    start_symbol: Token
    current_row: int
    current_position: int

    def __init__(self, grammar, start_symbol, input_tokens=None):
        self.grammar = grammar
        self.terminals = {
            token : {literal.value for rule in self.grammar[token] for literal in rule.rhs if self.is_terminal(literal)}
                    for token in self.grammar.keys()
        }
        self.chart = [[] for i in range(len(input_tokens) + 1)]
        self.input_tokens = input_tokens if input_tokens else []
        self.start_symbol = start_symbol
        self.current_row = 0
        self.current_position = 0 # i in the text

    def is_terminal(self, token: Token) -> bool:
        return not token in self.grammar

    def is_terminating(self, token: Token) -> bool:
        # constituents are nonterminals producing nonterminals
        return all([self.is_terminal(tok) for rule in self.grammar.get(token, []) for tok in rule.rhs])

    def insert(self, rule: Rule) -> None:
        rule.index = (rule.current_index, len(self.chart[rule.current_index]))
        if rule not in self.chart[rule.current_index]:
            self.chart[rule.current_index].append(rule)

    def predict(self, rule: Rule) -> None:
        tok = rule.get_current_token()
        if tok is None:
            raise ValueError('Predict cannot be called with a completed rule')
        for descendant_rule in self.grammar[tok]:
            new_rule = Rule(descendant_rule.lhs, descendant_rule.rhs, self.current_position, self.current_position,
                            previous_rule=rule.index)
            self.insert(new_rule)

    def extend_others(self, completed_rule: Rule) -> None:
        is_waiting = lambda rule: rule.get_current_token() == completed_rule.lhs
        waiting_rules = [rule for  rule in self.chart[completed_rule.start_index] if is_waiting(rule)]
        for waiting_rule in waiting_rules:
            self.insert(Rule(waiting_rule.lhs, waiting_rule.rhs,
                             waiting_rule.start_index, completed_rule.current_index, dot_index=waiting_rule.dot_index+1,
                             previous_rule=completed_rule.index, updated_rule=waiting_rule.index))

    def scan_input(self, rule) -> None:
        try:
            next_token = self.input_tokens[rule.current_index]
        except IndexError:
            return
        if next_token.token_type == rule.get_current_token() or next_token.value in self.terminals[rule.get_current_token()]:
            self.insert(Rule(rule.get_current_token(), [next_token], rule.current_index, rule.current_index+1, dot_index=1))

    def parse(self, input_tokens=None):
        if input_tokens:
            self.input_tokens = input_tokens
        for start_rule in self.grammar[self.start_symbol]:
            self.insert(start_rule)
        while self.current_position <= len(self.input_tokens):
            for rule in self.chart[self.current_position]:
                if rule.is_completed():
                    self.extend_others(rule)
                elif self.is_terminating(rule.get_current_token()):
                    self.scan_input(rule)
                else:
                    self.predict(rule)
            self.current_position += 1

    def is_complete(self) -> bool:
        if not any(self.chart):
            self.parse()
        completed = lambda rule: rule.lhs == self.start_symbol and rule.start_index == 0 \
                                 and rule.current_index == len(self.input_tokens)
        return any([completed(rule) for rule in self.chart[-1]])

    def __str__(self) -> str:
        def _token(index: int):
            return 'ℇ' if index <= 0 else self.input_tokens[index - 1]
        rows = [[f'Row {index}: {_token(index)}'] + [str(rule) for rule in row] for index, row in enumerate(self.chart)]
        return '\n'.join(['\n'.join(row) for row in rows])





