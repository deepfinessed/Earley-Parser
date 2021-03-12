from Rule import Token, Rule
from Parser import Parser

grammar = {
    Token("S")      : [Rule(Token("S"), [Token("NP"), Token("VP")])],
    Token("NP")     : [Rule(Token("NP"), [Token("N")]), Rule(Token("NP"), [Token("AttrNP")])],
    Token("VP")     : [Rule(Token("VP"), [Token("V")]), Rule(Token("VP"), [Token("VP"), Token("NP")])],
    Token("AttrNP") : [Rule(Token("AttrNP"), [Token("NP"), Token("N")])],
    Token("N")      : [Rule(Token("N"), [Token("_TERMINAL", "DB")]),
                       Rule(Token("N"), [Token("_TERMINAL", "shows")]),
                       Rule(Token("N"), [Token("_TERMINAL", "spread")]),
                       ],
    Token("V")      : [Rule(Token("V"), [Token("_TERMINAL", "shows")]),
                       Rule(Token("V"), [Token("_TERMINAL", "spread")])
                       ]
}

# terminals = {
#     Token("N") : {"DB", "shows", "spread"},
#     Token("V") : {"shows", "spread"}
# }

input_tokens = [Token("_TERMINAL", "DB"), Token("_TERMINAL", "shows"), Token("_TERMINAL", "spread")]

if __name__ == '__main__':
    test = Parser(grammar, Token("S"), input_tokens)

    test.parse()

    test_tree = test.parse_tree()

    print(test)



