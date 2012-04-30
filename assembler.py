import exceptions as exp
from grammars.tsm import *
from operations import operationToCode as opToCode
import program_scanner
from registers import Registers, nameToCode as regToCode
from utils import pack_bytes, unpack_bytes, clean_memory


class Assembler(object):
    def __init__(self, filename):
        self.filename = filename
        self.parser = TSM.parser()

        self.variables = {}
        self.labels = {}

        self.header = bytearray(b'\x84\x56\x49') 
        self.data = bytearray()
        self.program = bytearray()
        self.code = bytearray()

        self.data_length = 0
        self.data_section = True

        self.parse()
        self.compile()
    
    def parse(self):
        self.tree = self.parser.parse_file(self.filename) 

    def compile(self):
        self.sanitizer = Sanitizer(self.variables, self.data)
        for tree in self.tree:
            for el in tree.elements:
                if isinstance(el, Label):
                    self.labels[str(el[0])] = len(self.program)
                    next

                try:
                    if isinstance(el, Operation):
                      if self.data_section is True:
                          self.data_section = False
                          for d in unpack_bytes(self.data_length, 2, 10)[::-1]:
                              self.data.insert(0, d)

                      el = el[0]
                      args = [x for x in el.elements[1:] if str(x) != ',']
                      args = getattr(self.sanitizer, str(type(el)))(args)
                      getattr(self, str(type(el)))(args)
                    elif isinstance(el, Data):
                      args = [x for x in el.elements[1:] if str(x) != ',']
                      size = int(getattr(program_scanner, "%s_SIZE" % type(el.elements[0])))
                      args = getattr(self.sanitizer, "Data")(args, size)
                      getattr(self, "Data")(*args)
                except exp.AssemblyException:
                  print('Assembly Error')
                  raise
        self.code.extend(self.header)
        self.code.extend(self.data)
        self.code.extend(self.program)

    def Data(self, name, size, data):
        self.variables[name] = {'start': len(self.data), 'size': size}
        for d in data:
            self.data_length += len(d)
            self.data.extend(d)

    def MOV_R_R(self, args):
        a, b = args[0], args[1]
        self.program.append(opToCode['mov_reg_reg'])
        self.program.append(a)
        self.program.append(b)

    def MOV_R_L(self, args):
        a, b = args[0], args[1]
        self.program.append(opToCode['mov_reg_lit'])
        self.program.append(a)
        self.program.extend(b)

    def MOV_M_R(self, args):
        a, b = args[0], args[1]
        self.program.append(opToCode['mov_mem_reg'])
        self.program.append(a)
        if type(b) is bytearray:
            self.program.extend(b)
        elif type(b) is VariableIdentifier:
            try:
                self.program.extend(unpack_bytes(self.variables[str(b)]['start'], 2))
            except KeyError:
                raise exp.UnknownVariable

    def MOV_R_M(self, args):
        a, b = args[0], args[1]
        self.program.append(opToCode['mov_reg_mem'])
        self.program.append(a)
        if type(b) is bytearray:
            self.program.extend(b)
        elif type(b) is VariableIdentifier:
            try:
                self.program.extend(unpack_bytes(self.variables[str(b)]['start'], 2))
            except KeyError:
                raise exp.UnknownVariable


    def PUSH_R(self, args):
        pass

    def PUSH_L(self, args):
        pass

    def ADD_R_R(self, args):
        a, b = args[0], args[1]
        self.program.append(opToCode['add_reg_reg'])
        self.program.append(a)
        self.program.append(b)

    def SUB_R_R(self, args):
        a, b = args[0], args[1]
        self.program.append(opToCode['sub_reg_reg'])
        self.program.append(a)
        self.program.append(b)

    def SUB_R_L(self, args):
        a, b = args[0], args[1]
        self.program.append(opToCode['sub_reg_lit'])
        self.program.append(a)
        self.program.extend(b)

    def MUL_R_R(self, args):
        a, b = args[0], args[1]
        self.program.append(opToCode['mul_reg_reg'])
        self.program.append(a)
        self.program.append(b)

    def JMP_Z(self, args):
        a = args[0]
        self.program.append(opToCode['jmp_z'])
        self.program.extend(unpack_bytes(self.labels[a], 2))

    def JMP_NZ(self, args):
        a = args[0]
        self.program.append(opToCode['jmp_nz'])
        self.program.extend(unpack_bytes(self.labels[a], 2))

    def INT(self, args):
        a = args[0]
        self.program.append(opToCode['int'])
        self.program.append(a)

class Sanitizer(object):
    def __init__(self, variables, data):
        self.variables = variables
        self.data = data

    def getLiteral(self, arg):
        if type(arg) is OctalLiteral:
            return int(str(arg[1]), 16)
        elif type(arg) is DecimalLiteral:
            return int(str(arg[0]), 10)
        elif type(arg) is BinaryLiteral:
            return int(str(arg[0]), 2)
        elif type(arg) is MemoryLiteral:
            return unpack_bytes(clean_memory(str(arg)), 2)
        elif type(arg) is VariableIdentifier:
            return unpack_bytes(self.variables[str(arg)]['start'], 2)
        elif type(arg) is MemoryVariable:
            return unpack_bytes(self.variables[str(arg)[1:-1]]['start'], 2)

    def Data(self, args, size=1):
        a, b = args[0], args[1]
        b = filter(lambda x: str(x) != ',', b)
        clean_list = []
        for value in b:
            value = self.getLiteral(value)
            unpacked = unpack_bytes(value, size)

            if len(unpacked) > size:
                raise exp.InvalidDataSize

            clean_list.append(unpacked)
        return str(a), size, clean_list
        
    def MOV_R_R(self, args):
        try:
          return regToCode[str(args[0][0])], regToCode[str(args[1][0])]
        except KeyError:
          raise exp.InvalidOperandRegister

    def MOV_R_L(self, args):
        a, b = str(args[0]), self.getLiteral(args[1])
        b = unpack_bytes(b, Registers.sizeOf(a))
        if len(b) > Registers.sizeOf(a):
            raise exp.InvalidOperandSize
            
        return regToCode[a], b
    
    def MOV_M_R(self, args):
        a, b = args[0], args[1]
        return regToCode[b], self.getLiteral(a)
    
    def MOV_R_M(self, args):
        b, a = args[0], args[1]
        return regToCode[str(b)], self.getLiteral(a)
    
    def PUSH_R(self, args):
        pass
    
    def PUSH_L(self, args):
        pass
    
    def ADD_R_R(self, args):
        a, b = str(args[0]), str(args[1])

        if Registers.sizeOf(a) != Registers.sizeOf(b):
            raise exp.RegisterSizeMismatch

        try:
            return regToCode[str(args[0])], regToCode[str(args[1])]
        except KeyError:
            raise exp.InvalidOperandRegister

    def ADD_R_L(self, args):
        pass
    
    def SUB_R_R(self, args):
        a, b = str(args[0]), str(args[1])

        if Registers.sizeOf(a) != Registers.sizeOf(b):
            raise exp.RegisterSizeMismatch

        try:
            return regToCode[str(args[0])], regToCode[str(args[1])]
        except KeyError:
            raise exp.InvalidOperandRegister
    
    def SUB_R_L(self, args):
        a, b = str(args[0]), self.getLiteral(args[1])

        if ((len(hex(b)) - 2) + 0.5) > Registers.sizeOf(a):
            raise exp.RegisterSizeMismatch

        try:
            return regToCode[str(args[0])], unpack_bytes(b, Registers.sizeOf(a))
        except KeyError:
            raise exp.InvalidOperandRegister
    
    def MUL_R_R(self, args):
        a, b = str(args[0]), str(args[1])

        if Registers.sizeOf(a) != Registers.sizeOf(b):
            raise exp.RegisterSizeMismatch

        try:
            return regToCode[str(args[0])], regToCode[str(args[1])]
        except KeyError:
            raise exp.InvalidOperandRegister

    def JMP_Z(self, args):
      return str(args[0]),

    def JMP_NZ(self, args):
      return str(args[0]),

    def INT(self, args):
      a = self.getLiteral(args[0])
      if len(unpack_bytes(a)) != 1:
          raise exp.InvalidInterrupt

      return self.getLiteral(args[0]),
