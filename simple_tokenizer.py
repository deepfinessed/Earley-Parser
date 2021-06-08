from typing import List

from Rule import Token

class Simple_Tokenizer:
    """
    A simple tokenizer for custom grammars - it merely splits on whitespace and returns the words as tokens
    """

    text: str

    def __init__(self, text: str) -> None:
        self.text = text

    def tokenize(self) -> List[Token]:
        return [Token("_TERMINAL", value=token) for token in self.text.split()]
