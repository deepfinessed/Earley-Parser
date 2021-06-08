from argparse import ArgumentParser
from typing import Callable, List, Dict, Optional, Set, Tuple

import EBNF_Grammar
from EBNF_Tokenizer import EBNF_Tokenizer
from EBNF_Visitor import EBNF_Visitor
from Rule import Token, Rule
import simple_sentence
from simple_tokenizer import Simple_Tokenizer
from Tree import Node

class Parser:
    """
    An Earley parser implemented based on the algorithm in the text

    Attributes:
        grammar             A dictionary containing our base ruleset
        terminals           A dictionary mapping terminal tokens to their values, generated from grammar
        chart               The chart for our parse
        input_tokens        The string to be parsed
        current_position    The position in the parse
    """

    grammar: Dict[Token, List[Rule]]
    terminals: Dict[Token, Set[str]]
    chart: List[List[Rule]]
    input_tokens: List[Token]
    start_symbol: Token
    current_position: int


    def __init__(self, grammar: Dict[Token, List[Rule]], start_symbol: Token,
                 input_tokens: Optional[List[Token]]=None) -> None:
        self.grammar = grammar
        self.terminals = {
            token : {literal.value for rule in self.grammar[token] for literal in rule.rhs if self.is_terminal(literal)}
                    for token in self.grammar.keys()
        }
        if input_tokens:
            self.chart = [[] for _ in range(len(input_tokens) + 1)]
        self.input_tokens = input_tokens if input_tokens else []
        self.start_symbol = start_symbol
        self.current_position = 0 # i in the text

    def is_terminal(self, token: Token) -> bool:
        return not token in self.grammar

    def is_terminating(self, token: Token) -> bool:
        # constituents are nonterminals producing nonterminals
        return all([self.is_terminal(tok) for rule in self.grammar.get(token, []) for tok in rule.rhs])

    def insert(self, rule: Rule) -> None:
        rule.index = (rule.current_index, len(self.chart[rule.current_index]))
        # Avoid repeatedly inserting rules that are 'from xxx'
        if rule.updated_rule or rule not in self.chart[rule.current_index]:
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

    def scan_input(self, rule: Rule) -> None:
        try:
            next_token = self.input_tokens[rule.current_index]
        except IndexError:
            return
        if next_token == rule.get_current_token()\
                or (rule.get_current_token() in self.terminals and next_token.value in self.terminals[rule.get_current_token()]):
            self.insert(Rule(rule.get_current_token(), [next_token], rule.current_index, rule.current_index+1, dot_index=1))

    def parse(self, input_tokens: Optional[List[Token]]=None) -> None:
        if input_tokens:
            self.input_tokens = input_tokens
            self.chart = [[] for _ in range(len(input_tokens) + 1)]
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
        completed: Callable[[Rule], bool] = lambda rule: rule.lhs == self.start_symbol and rule.start_index == 0 \
                                 and rule.current_index == len(self.input_tokens)
        return any([completed(rule) for rule in self.chart[-1]])

    def get_rule(self, index: Optional[Tuple[int, int]]) -> Rule:
        if index is None:
            raise ValueError('None index passed to get_rule')
        row, idx = index
        try:
            return self.chart[row][idx]
        except IndexError as e:
            print(f'Invalid rule access at {index}')
            raise e


    def __make_node(self, rule: Rule) -> Node[Token]:

        # Handle all previous rules
        previous_siblings = []
        iterator = rule
        while iterator.updated_rule:
            previous_siblings.append(iterator)
            iterator = self.get_rule(iterator.updated_rule)

        # Make the node corresponding to the input rule
        new_parent_node = Node(rule.lhs)

        if previous_siblings:
            while previous_siblings:
                sibling = previous_siblings.pop()
                # This check is needed to avoid double counting terminals at the end of a tagged string
                if not self.is_terminal(sibling.lhs):
                    new_parent_node.append_node(self.__make_node(self.get_rule(sibling.previous_rule)))
        else:
            previous_token = rule.get_previous_token()
            if previous_token:
                new_parent_node.value = Token(rule.lhs.token_type, value=previous_token.value)
            # if previous_token and self.is_terminal(previous_token) and not previous_token == rule.lhs:
            #     new_parent_node.add_child(rule.get_previous_token())

        return new_parent_node

    def parse_tree(self) -> Optional[Node[Token]]:
        if not any(self.chart):
            self.parse()
        try:
            completed = lambda rule: rule.lhs == self.start_symbol and rule.start_index == 0 \
                                     and rule.current_index == len(self.input_tokens)
            completed_parse = next(rule for rule in self.chart[-1] if completed(rule))
            return self.__make_node(completed_parse)
        except StopIteration:
            return None

    def parse_forest(self) -> List[Node[Token]]:
        if not any(self.chart):
            self.parse()
        completed = lambda rule: rule.lhs == self.start_symbol and rule.start_index == 0 \
                                 and rule.current_index == len(self.input_tokens)
        return [self.__make_node(rule) for rule in self.chart[-1] if completed(rule)]

    def __str__(self) -> str:
        def _token(index: int) -> str:
            return 'ℇ' if index <= 0 else self.input_tokens[index - 1]
        rows = [[f'Row {index}: {_token(index)}'] + [str(rule) for rule in row] for index, row in enumerate(self.chart)]
        return '\n'.join(['\n'.join(row) for row in rows])



if __name__ =='__main__':
    parser = ArgumentParser(description='Parse a grammar and generate corresponding trees')
    parser.add_argument('-g', '--grammar-file', help='Read a grammar file written in EBNF')
    parser.add_argument('-s', '--start-symbol', help='The start symbol for the grammar, default S', default='S')
    parser.add_argument('input_file', help='File containing the string to be parsed')

    args = parser.parse_args()

    if args.grammar_file:
        with open(args.grammar_file) as grammar_file:
            ebnf_tokenizer = EBNF_Tokenizer(grammar_file)
            tokens = ebnf_tokenizer.tokenize()
            grammar_parser = Parser(EBNF_Grammar.grammar, EBNF_Grammar.start_symbol)
            grammar_parser.parse(tokens)
            grammar_tree = grammar_parser.parse_tree()
            if grammar_tree is None:
                raise ValueError('There is no valid parse')
            grammar_visitor = EBNF_Visitor()
            new_grammar = grammar_visitor.generate_grammar(grammar_tree)
    else:
        new_grammar = simple_sentence.grammar

    start_symbol = args.start_symbol

    with open(args.input_file) as input_file:
        tokenizer = Simple_Tokenizer(input_file.read())
        tokens = tokenizer.tokenize()
        earley_parser = Parser(new_grammar, Token(start_symbol), tokens)

    earley_parser.parse()
    print(earley_parser)

















