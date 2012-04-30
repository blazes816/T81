from modgrammar import *
from grammars.identifiers import *


class OctalLiteral(Grammar):
    grammar = (L('0x'), WORD('[0-9a-f]'), OPTIONAL('h'))

class DecimalLiteral(Grammar):
    grammar = (WORD('[0-9]'), L('d'))

class BinaryLiteral(Grammar):
    grammar = (WORD('[0-1]'), L('b'))

class IntegerLiteral(Grammar):
    grammar = (OctalLiteral | DecimalLiteral | BinaryLiteral)
    grammar_collapse = True

class MemoryLiteral(Grammar):
    grammar = (L('['), OctalLiteral, L(']'))

class MemoryVariable(Grammar):
    grammar = (L('['), VariableIdentifier, L(']'))
