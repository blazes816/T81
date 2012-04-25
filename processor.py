from copy import copy

import debugger
import exceptions as exp
from operations import Operations
from program_scanner import ProgramScanner
from registers import Registers
from utils import pack_bytes, unpack_bytes

REGISTERS = {'eax': 0x00, 'ebx': 0x00, 'ecx': 0x00, 'edx': 0x0}
OPCODE_SIZE = 1

class Processor(object):

    def __init__(self, debug=False):
        self.name = "Untitled Program"
        # Initialize critical elements: registers, memory, etc
        self.debug = debug
        self.program_memory = bytearray()#[]
        self.memory = bytearray()
        self.registers = Registers()

    def load(self, code, name=None):
        if name is not None:
            self.name = name

        get_bytes = lambda x: [code.pop(0) for i in range(x)]

        # Check file header
        self.check_header(get_bytes(3))

        data_size = pack_bytes(get_bytes(2))
        for i in range(0, data_size):
            self.memory.append(code.pop(0))

        self.program_memory.extend(code)

    def load_from_file(self, filename):
      with open(filename, "rb") as f:
        self.load(f.read(), name=filename)

    def check_header(self, header):
        if bytearray(header) != bytearray(b'\x84\x56\x49'):
            raise exp.InvalidFile

    def run(self):
        self.program_scanner = ProgramScanner(self.program_memory, self.registers)
        self.ops = Operations(self.program_scanner, self.memory, self.registers)

        print("\nInitial Configuration:")
        print(self)

        print("Executing: %s\n" % self.name) 
        while 1:
            try:
              opcode = self.program_scanner.nextOpcode()
            except exp.EndOfProgram:
              break
            op = self.ops.fromCode(opcode)
            op()

        print("Final Configuration:")
        print(self)

    def __repr__(self):
        string = "\tMain Memory:\t%s\n" % str(self.memory)
        string += "\tProgram Memory:\t%s\n" % str(self.program_memory)
        string += "\tRegisters:\t%s\n" % str(self.registers)
        return string
        
