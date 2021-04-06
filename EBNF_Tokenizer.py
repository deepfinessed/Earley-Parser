import re
from typing import List, Optional, TextIO
import sys
from Rule import Token


class Char_Reader:
    """
    A simple text reader that returns one character at a time from a file
    """

    text: str
    line_number: int
    char_index: int
    horiz_position: int

    def __init__(self, source):
        self.text = source.read()
        self.char_index = 0
        self.line_number = 0
        self.horiz_position = 0

    def peek(self) -> str:
        try:
            return self.text[self.char_index]
        except IndexError:
            return ''

    def read(self) -> str:
        try:
            char = self.text[self.char_index]
        except IndexError:
            return ''
        self.horiz_position += 1
        if char == '\n':
            self.line_number += 1
            self.horiz_position = 0
        self.char_index += 1
        return char

class EBNF_Tokenizer:
    """
    A tokenizer for EBNF_Grammar.py. It distinguishes identifiers, terminals, and symbols.
    """
    reader: Char_Reader
    quotes: List[str]

    def __init__(self, source):
        self.reader = Char_Reader(source)
        symbols = ["[" , "]" , "{" , "}" , "(" , ")" , "<" , ">", "=" , "," , "." , "," , ";", "=", "|"]
        self.symbols = {symbol : Token("_TERMINAL", value=symbol) for symbol in symbols}
        self.quotes = []


    def next_token(self) -> Optional[Token]:
        char = self.reader.read()
        if not char:
            return None
        while re.match(r'\s', char):
            char = self.reader.read()
            if not char:
                return None
        if char in self.symbols:
            return self.symbols[char]
        tok = char
        if re.match(r'[\'\"]', char):
            quote = char
            char = self.reader.read()
            while char != quote:
                tok += char
                char = self.reader.read()
                if not char:
                    raise ValueError("Error: File ended on an open quote")
            tok += char
            # strip the quotes from our terminals
            return Token("terminal", value=tok[1:-1])
        while re.match(r'[A-Za-z0-9_]', self.reader.peek()):
            char = self.reader.read()
            tok += char
            if not char:
                raise ValueError("Error: File ended while processing an identifier")
        return Token("identifier", value=tok)

    def tokenize(self) -> List[Token]:
        tokens = []
        token = self.next_token()
        while not token is None:
            tokens.append(token)
            token = self.next_token()
        return tokens






if __name__ == '__main__':
    with open(sys.argv[2]) as f:
        test = EBNF_Tokenizer(f)
        print(*test.tokenize(), sep='\n')


