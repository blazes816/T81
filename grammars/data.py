from modgrammar import *
from grammars.literals import *
from grammars.identifiers import *

class DB(Grammar):
    grammar = ('DB')

class DW(Grammar):
    grammar = ('DD')

class DD(Grammar):
    grammar = ('DW')

class Type(Grammar):
    grammar = (DB | DW | DD)
    grammar_collapse = True

class Data(Grammar):
    grammar = (Type, VariableIdentifier, LIST_OF(IntegerLiteral, sep=','))
