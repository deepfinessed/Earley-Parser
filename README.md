# Earley Parser

## Description

This is an Earley Parser, or chart parser, made to illustrate the algorithm discussed in class. It is a work in progress

## Usage

Try the parser with ```python Parser.py FILE```

to see it parse `FILE` with a default simplified set of English grammar rules.

The parser also supports specifying a grammar via EBNF.

You can see this functionality with ```python Parser.py -g grammar.ebnf rogue_robot.txt```

## Ambiguous Parses

Since handling ambiguous parses is one of the strengths of Earley parsers,
the parser can return multiple correct parsers if they exist.  

You can see an example of this in the console with

```python Parser.py -g microscope.ebnf microscope.txt```

The final row of the printed parse table:

```
Row 7: "microscope"
7.a N          → "microscope"•        [ 6,  7] scan
7.b NP         → Det N•               [ 5,  7] 7.a/6.b
7.c PP         → Prep NP•             [ 4,  7] 7.b/5.b
7.d NP         → NP •PP               [ 5,  7] 7.b/5.e
7.e NP         → NP PP•               [ 2,  7] 7.c/4.d
7.f VP         → VP PP•               [ 1,  7] 7.c/4.f
7.g PP         → •Prep NP             [ 7,  7] from 7.d
7.h VP         → V NP•                [ 1,  7] 7.e/2.c
7.i NP         → NP •PP               [ 2,  7] 7.e/2.h
7.j S          → NP VP•               [ 0,  7] 7.f/1.c
7.k VP         → VP •PP               [ 1,  7] 7.f/1.f
7.l S          → NP VP•               [ 0,  7] 7.h/1.c
7.m VP         → VP •PP               [ 1,  7] 7.h/1.f
```

Reveals 2 complete parses: 7.j and 7.l that correspond to different
interpretations of the sentence (does Jen have the microscope, or does the man).

The resulting parse trees are also available.