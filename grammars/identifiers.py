from modgrammar import *

class Identifier(Grammar):
    grammar = (WORD('a-z_', 'a-zA-Z0-9_'))

class VariableIdentifier(Grammar):
    grammar = (Identifier)

class Label(Grammar):
    grammar = (Identifier, L(':'))
