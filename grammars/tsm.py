from modgrammar import *
from grammars.literals import *
from grammars.identifiers import *
from grammars.registers import *
from grammars.operations import *
from grammars.data import *

class Comment(Grammar):
    grammar = G(L('#'), ANY_EXCEPT(';'), L(';')) |\
                G(L('/*'), ANY_EXCEPT('*/'), L('*/'))

class OperationsSection(Grammar):
    grammar = (REPEAT(Comment | Operation | Label, collapse=True))
    grammar_collapse = True


class DataSection(Grammar):
    grammar = (REPEAT(Comment | Data, collapse=True))
    grammar_collapse = True

class TSM(Grammar):
    grammar = (OPTIONAL(DataSection), OperationsSection)
