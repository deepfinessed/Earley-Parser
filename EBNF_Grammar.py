from Rule import Token, Rule

"""
This is the EBNF grammar, written so it is understandable by Parser.py. It is based on the rules the comment
at the bottom of this file.

To avoid exploding our poor parser and generating absolutely silly parse trees, we will delegate responsibility for 
identifying terminal and identifier symbols to the parser.
"""

grammar = {
    Token("grammar")   : [Rule(Token("grammar"), [Token("rule"), Token("grammar")]),
                        Rule(Token("grammar"), [Token("rule")])],
    Token("rule")      : [Rule(Token("rule"), [Token("lhs"), Token("_TERMINAL", "="), Token("rhs"), Token("_TERMINAL", ";")])],
    Token("lhs")       : [Rule(Token("lhs"), [Token("identifier")])],
    Token("rhs")       : [Rule(Token("rhs"), [Token("or")]),
                          Rule(Token("rhs"), [Token("sequence")])
                        ],
    Token("sequence")  : [Rule(Token("sequence"), [Token("term")]),
                          Rule(Token("sequence"), [Token("concat")])
                          ],
    Token("term")      : [Rule(Token("term"), [Token("identifier")]),
                          Rule(Token("term"), [Token("terminal")]),
                          Rule(Token("term"), [Token("optional")]),
                          Rule(Token("term"), [Token("repitition")]),
                          Rule(Token("term"), [Token("group")]),
                        ],
    Token("optional")  : [Rule(Token("optional"), [Token("_TERMINAL", "["), Token("rhs"), Token("_TERMINAL", "]")])],
    Token("repitition"): [Rule(Token("repitition"), [Token("_TERMINAL", "{"), Token("rhs"), Token("_TERMINAL", "}")])],
    Token("group")     : [Rule(Token("group"), [Token("_TERMINAL", "("), Token("rhs"), Token("_TERMINAL", ")")])],
    Token("or")        : [Rule(Token("or"), [Token("sequence"), Token("_TERMINAL", "|"), Token("rhs")])],
    Token("concat")    : [Rule(Token("concat"), [Token("term"), Token("_TERMINAL", ","), Token("sequence")])],
    Token("identifier"): [],
    Token("terminal")  : [],
}

start_symbol = Token("grammar")

"""
The following is the EBNF grammar for EBNF on wikipedia:

letter = "A" | "B" | "C" | "D" | "E" | "F" | "G"
       | "H" | "I" | "J" | "K" | "L" | "M" | "N"
       | "O" | "P" | "Q" | "R" | "S" | "T" | "U"
       | "V" | "W" | "X" | "Y" | "Z" | "a" | "b"
       | "c" | "d" | "e" | "f" | "g" | "h" | "i"
       | "j" | "k" | "l" | "m" | "n" | "o" | "p"
       | "q" | "r" | "s" | "t" | "u" | "v" | "w"
       | "x" | "y" | "z" ;
digit = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;
symbol = "[" | "]" | "{" | "}" | "(" | ")" | "<" | ">"
       | "'" | '"' | "=" | "|" | "." | "," | ";" ;
character = letter | digit | symbol | "_" ;

identifier = letter , { letter | digit | "_" } ;
terminal = "'" , character , { character } , "'"
         | '"' , character , { character } , '"' ;

lhs = identifier ;
rhs = identifier
     | terminal
     | "[" , hhs , "]"
     | "{" , rhs , "}"
     | "(" , rhs , ")"
     | rhs , "|" , rhs
     | rhs , "," , rhs ;

rule = lhs , "=" , rhs , ";" ;
grammar = { rule } ;

________________________________________________________________________________-

Because the sketch grammar above is inconsistent with a common sense reading of
most EBNF rules, it was rewritten to produce a different operator precedence as follows:

ORIGINAL RULES: 

lhs = identifier ;
rhs = identifier
     | terminal
     | optional
     | repitition
     | group
     | or
     | concat

optional = "[" , hhs , "]";

repitition = "{" , rhs , "}";

group = "(" , rhs , ")";

or = rhs , "|" , rhs;

concat = rhs , "," , rhs ;

rule = lhs , "=" , rhs , ";" ;
grammar = { rule } ;

________________________________________________________________________________

NEW RULES:

~~~~HIGHEST PRECEDENCE
~~~~group(), repitition{}, optional[], terminal, identifier (term)
~~~~concat ','                                              (sequence)
~~~~or '|'                                                  (rhs)
~~~~LOWEST PRECEDENCE                                       

lhs = identifier ;
rhs = sequence
     | or
     
sequence = term | concat

term = optional | repitition | group | identifier | terminal

concat = term "," sequence

optional = "[" , rhs , "]";

repitition = "{" , rhs , "}";

group = "(" , rhs , ")";

or = sequence , "|" , rhs;

rule = lhs , "=" , rhs , ";" ;
grammar = { rule } ;


"""
