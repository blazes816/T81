from modgrammar import *

class Register(Grammar):
    grammar = (L('eax') | L('ax') | L('ah')| L('al') |\
               L('ebx') | L('bx') | L('bh')| L('bl') |\
               L('ecx') | L('cx') | L('ch')| L('cl') |\
               L('edx') | L('dx') | L('dh')| L('dl'))
