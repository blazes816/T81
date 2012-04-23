import exceptions as exp
from grammars.tsm import *
from operations import operationToCode as opToCode
from registers import Registers, nameToCode as regToCode
from utils import unpack_bytes

class Assembler(object):
    def __init__(self, filename):
        self.filename = filename
        self.parser = TSM.parser()
        self.code = bytearray(b'\x84\x56\x49')
        self.parse()
        self.compile()
    
    def parse(self):
        self.tree = self.parser.parse_file(self.filename) 

    def compile(self):
        for i in self.tree:
            for j in i.elements:
                args = [x for x in j.elements[1:] if str(x) != ',']
                args = getattr(Sanitizer, str(type(j)))(args)
                getattr(self, str(type(j)))(args)

    def bytes(self):
        return self.code

    def MOV_R_R(self, args):
        a, b = args[0], args[1]
        self.code.append(opToCode['mov_reg_reg'])
        self.code.append(a)
        self.code.append(b)

    def MOV_R_L(self, args):
        a, b = args[0], args[1]
        self.code.append(opToCode['mov_reg_lit'])
        self.code.append(a)
        self.code.extend(b)

    def MOV_M_R(self, args):
        a, b = args[0], args[1]
        self.code.append(opToCode['mov_mem_reg'])
        self.code.append(a)
        self.code.extend(b)

    def PUSH_R(self, args):
        pass

    def PUSH_L(self, args):
        pass

class Sanitizer(object):
    @staticmethod
    def MOV_R_R(args):
        try:
          return regToCode[str(args[0][0])], regToCode[str(args[1][0])]
        except KeyError:
          raise exp.InvalidOperandRegister

    def MOV_R_L(args):
        a, b = str(args[0]), None

        if type(args[1]) is OctalLiteral:
            b = int(str(args[1][1]), 16)
        elif type(args[1]) is DecimalLiteral:
            b = int(str(args[1][0]), 10)
        elif type(args[1]) is BinaryLiteral:
            b = int(str(args[1][0]), 2)
        
        b = unpack_bytes(b)
        b_hex = ''.join(''.join([hex(x) for x in b]).split('0x'))

        if (len(b_hex) / 2) + 0.5 < Registers.sizeOf(a):
            raise exp.InvalidOperandSize
            
        return regToCode[a], b

    def MOV_M_R(args):
        a, b = str(args[0]), str(args[1])
        a = unpack_bytes(a, size=Registers.sizeOf(b))
        return regToCode[b], a

    def PUSH_R(args):
        pass

    def PUSH_L(args):
        pass
