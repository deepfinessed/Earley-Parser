from Rule import Token

class Simple_Tokenizer:
    """
    A simple tokenizer for custom grammars - it merely splits on whitespace and returns the words as tokens
    """

    text: str

    def __init__(self, text):
        self.text = text

    def tokenize(self):
        return [Token("_TERMINAL", value=token) for token in self.text.split()]
