from modgrammar import *
from grammars.registers import *
from grammars.literals import *
from grammars.identifiers import *

class MOV_R_R(Grammar):
    grammar = (L('mov'), Register, L(','), Register)

class MOV_R_L(Grammar):
    grammar = (L('mov'), Register, L(','), IntegerLiteral | VariableIdentifier)

class MOV_M_R(Grammar):
    grammar = (L('mov'), (MemoryLiteral | MemoryVariable), L(','), Register)

class MOV_R_M(Grammar):
    grammar = (L('mov'), Register, L(','), (MemoryLiteral | MemoryVariable))

class PUSH_R(Grammar):
    grammar = (L('push'), Register)

class PUSH_L(Grammar):
    grammar = (L('push'), IntegerLiteral)

class ADD_R_R(Grammar):
    grammar = (L('add'), Register, L(','), Register)

class SUB_R_R(Grammar):
    grammar = (L('sub'), Register, L(','), Register)

class SUB_R_L(Grammar):
    grammar = (L('sub'), Register, L(','), IntegerLiteral)

class MUL_R_R(Grammar):
    grammar = (L('mul'), Register, L(','), Register)

class JMP_Z(Grammar):
    grammar = (L('jmpz'), Identifier)

class JMP_NZ(Grammar):
    grammar = (L('jmpnz'), Identifier)

class INT(Grammar):
    grammar = (L('int'), IntegerLiteral)

class Operation(Grammar):
    grammar = (MOV_R_R | MOV_R_L | MOV_M_R | MOV_R_M | PUSH_R | PUSH_L | ADD_R_R |\
               SUB_R_R | SUB_R_L | MUL_R_R | JMP_Z | JMP_NZ | INT, L(';'))
