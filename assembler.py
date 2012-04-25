import exceptions as exp
from grammars.tsm import *
from operations import operationToCode as opToCode
import program_scanner
from registers import Registers, nameToCode as regToCode
from utils import unpack_bytes, clean_memory

class Assembler(object):
    def __init__(self, filename):
        self.filename = filename
        self.parser = TSM.parser()
        self.code = bytearray(b'\x84\x56\x49')
        self.variables = {}
        self.data_length = 0
        self.data_section = True

        self.parse()
        self.compile()
    
    def parse(self):
        self.tree = self.parser.parse_file(self.filename) 
        print("Parsing complete")

    def compile(self):
        for tree in self.tree:
            for el in tree.elements:
                try:
                    if isinstance(el, Operation):
                      if self.data_section is True:
                          self.data_section = False
                          for d in unpack_bytes(self.data_length, 2, 10)[::-1]:
                              self.code.insert(3, d)

                      el = el[0]
                      args = [x for x in el.elements[1:] if str(x) != ',']
                      args = getattr(Sanitizer, str(type(el)))(args)
                      getattr(self, str(type(el)))(args)
                    elif isinstance(el, Data):
                      args = [x for x in el.elements[1:] if str(x) != ',']
                      size = int(getattr(program_scanner, "%s_SIZE" % type(el.elements[0])))
                      args = getattr(Sanitizer, "Data")(args, size)
                      getattr(self, "Data")(*args)
                except exp.AssemblyException:
                  print('Assembly Error')
                  print(el)
                  raise
        print("Compilation complete")

    def Data(self, name, data):
        self.variables[name] = {'start': len(self.code) - 3}
        for d in data:
            self.data_length += len(d)
            self.code.extend(d)

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
        if type(b) is bytearray:
            self.code.extend(b)
        elif type(b) is VariableIdentifier:
            try:
                self.code.extend(unpack_bytes(self.variables[str(b)]['start'], 2))
            except KeyError:
                raise exp.UnknownVariable


    def PUSH_R(self, args):
        pass

    def PUSH_L(self, args):
        pass

    def ADD_R_R(self, args):
        a, b = args[0], args[1]
        self.code.append(opToCode['add_reg_reg'])
        self.code.append(a)
        self.code.append(b)

class Sanitizer(object):
    @staticmethod
    def Data(args, size=1):
        a, b = str(args[0]), [x.lstrip().rstrip() for x in str(args[1]).split(',')]
        clean_list = []
        for value in b:
            value = int(value, 16)
            unpacked = unpack_bytes(value, size)
            if len(unpacked) > size:
                raise exp.InvalidDataSize
            clean_list.append(unpacked)
        return a, clean_list
                    
        
    @staticmethod
    def MOV_R_R(args):
        try:
          return regToCode[str(args[0][0])], regToCode[str(args[1][0])]
        except KeyError:
          raise exp.InvalidOperandRegister

    @staticmethod
    def MOV_R_L(args):
        a, b = str(args[0]), None

        if type(args[1]) is OctalLiteral:
            b = int(str(args[1][1]), 16)
        elif type(args[1]) is DecimalLiteral:
            b = int(str(args[1][0]), 10)
        elif type(args[1]) is BinaryLiteral:
            b = int(str(args[1][0]), 2)
        
        b = unpack_bytes(b, Registers.sizeOf(a))
        if len(b) > Registers.sizeOf(a):
            raise exp.InvalidOperandSize
            
        return regToCode[a], b

    @staticmethod
    def MOV_M_R(args):
        a, b = args[0], str(args[1])
        if type(a) is MemoryLiteral:
            a = unpack_bytes(clean_memory(str(a)), size=2)
        return regToCode[b], a

    @staticmethod
    def PUSH_R(args):
        pass

    @staticmethod
    def PUSH_L(args):
        pass

    @staticmethod
    def ADD_R_R(args):
        a, b = str(args[0]), str(args[1])

        if Registers.sizeOf(a) != Registers.sizeOf(b):
            raise exp.RegisterSizeMismatch

        try:
            return regToCode[str(args[0])], regToCode[str(args[1])]
        except KeyError:
            raise exp.InvalidOperandRegister

    @staticmethod
    def ADD_R_L(args):
        pass
