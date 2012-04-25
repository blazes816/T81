from modgrammar import *

class OctalLiteral(Grammar):
    grammar = (L('0x'), WORD('[0-9a-f]'))

class DecimalLiteral(Grammar):
    grammar = (WORD('[0-9]'), L('d'))

class BinaryLiteral(Grammar):
    grammar = (WORD('[0-1]'), L('b'))

class Literal(Grammar):
    grammar = (OctalLiteral | DecimalLiteral | BinaryLiteral)
    grammar_collapse = True

class MemoryLiteral(Grammar):
    grammar = (L('['), OctalLiteral, L(']'))



class VariableIdentifier(Grammar):
    grammar = (WORD('a-z_', 'a-zA-Z0-9_'))


class Register(Grammar):
    grammar = (L('eax') | L('ax') | L('ah')| L('al') |\
               L('ebx') | L('bx') | L('bh')| L('bl') |\
               L('ecx') | L('cx') | L('ch')| L('cl') |\
               L('edx') | L('dx') | L('dh')| L('dl'))

class MOV_R_R(Grammar):
    grammar = (L('mov'), Register, L(','), Register)

class MOV_R_L(Grammar):
    grammar = (L('mov'), Register, L(','), Literal)

class MOV_M_R(Grammar):
    grammar = (L('mov'), (MemoryLiteral | VariableIdentifier), L(','), Register)

class PUSH_R(Grammar):
    grammar = (L('push'), Register)

class PUSH_L(Grammar):
    grammar = (L('push'), Literal)

class ADD_R_R(Grammar):
    grammar = (L('add'), Register, L(','), Register)



class Operation(Grammar):
    grammar = (MOV_R_R | MOV_R_L | MOV_M_R | PUSH_R | PUSH_L | ADD_R_R, L(';'))

class OperationsSection(Grammar):
    grammar = (REPEAT(Operation, collapse=True))
    grammar_collapse = True


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
    grammar = (Type, VariableIdentifier, LIST_OF(OctalLiteral, sep=','))

class DataSection(Grammar):
    grammar = (REPEAT(Data, collapse=True))
    grammar_collapse = True

class TSM(Grammar):
    grammar = (OPTIONAL(DataSection), OperationsSection)
