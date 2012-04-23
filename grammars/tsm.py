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

class Memory(Grammar):
    grammar = (OctalLiteral)




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
    grammar = (L('mov'), Memory, L(','), Register)

class PUSH_R(Grammar):
    grammar = (L('push'), Register)

class PUSH_L(Grammar):
    grammar = (L('push'), Literal)



class Command(Grammar):
    grammar = (MOV_R_R | MOV_R_L | MOV_M_R | PUSH_R | PUSH_L, L(';'))
    grammar_collapse = True

class OperationsSection(Grammar):
    grammar = (REPEAT(Command, collapse=True))
    grammar_collapse = True

class TSM(Grammar):
    grammar = (OperationsSection)
