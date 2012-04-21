from copy import copy

import debugger
import exceptions as exp
from operations import Operations
from program_scanner import ProgramScanner
from registers import Registers

REGISTERS = {'eax': 0x00, 'ebx': 0x00, 'ecx': 0x00, 'edx': 0x0}
OPCODE_SIZE = 1

class Processor(object):

    def __init__(self, debug=False):
        # Initialize critical elements: registers, memory, etc
        self.debug = debug
        self.program_memory = []
        self.main_memory = []
        self.registers = Registers()

    def load(self, filename):
      with open(filename, "rb") as f:
        # Check file header
        if (f.read(3) != b'\x84\x56\x49'):
            raise exp.InvalidFile

        # Load our program byte by byte
        # Use next_byte closure to simplify the process of converting
        # from written binary to Python hex integer
        byte = 0x00
        def next_byte():
            nonlocal byte
            byte = f.read(1)
            byte = hex(byte[0]) if len(byte) == 1 else None
            return byte

        while next_byte():
            self.program_memory.append(byte)

    def load_from_bytes(self, byte_array):
        self.program_memory = copy(byte_array)

    def run(self):
        self.program_scanner = ProgramScanner(self.program_memory, self.registers)
        self.ops = Operations(self.program_scanner, self.main_memory,
                              self.registers)
        print(self.registers)
        while 1:
            try:
              opcode = self.program_scanner.nextOpcode()
            except exp.EndOfProgram:
              break
            op = self.ops.fromCode(opcode)
            op()
            print(self.registers)
        pass
