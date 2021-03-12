# Earley Parser

## Description

This is an Earley Parser, or chart parser, made to illustrate the algorithm discussed in class. It is a work in progress

## Usage

Try the parser with ```python Parser.py FILE```

to see it parse `FILE` with a default simplified set of English grammar rules.

The parser also supports specifying a grammar via EBNF.

You can see this functionality with ```python Parser.py -g grammar.ebnf rogue_robot.txt```

## Operator Precedence

There is not extensive documentation on EBNF operator precedence.
Based on some sketch EBNF grammar, the parser currently treats all operators as having equal precedence,
meaning that parenthesis are frequently required:  
```NP = N | Det, N | NP, PP | Name; ``` would be interpreted by
many as NP is N or Det, N or NP, PP or Name, but this parser would not
see it that way - the rule would have to be written:  

```NP = N | (Det, N) | (NP, PP) | Name; ```

This is counterintuitive, and one of the planned improvements
is to change the EBNF grammar rules to have the ',' operator
and the '|' operator at different precedence levels.