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
        # Initialize critical elements: registers, memory, etc
        self.debug = debug
        self.program_memory = []
        self.memory = bytearray()
        self.registers = Registers()

    def load(self, filename):
      with open(filename, "rb") as f:
        # Eat file header
        f.read(3)

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

        self.check_header()

    def load_from_bytes(self, byte_array):
        self.program_memory = copy(byte_array)
        self.check_header()

    def check_header(self):
        header = bytearray([self.program_memory.pop(0) for x in range(3)])
        if header == bytearray(b'\x84\x56\x49'):
            return True
        raise exp.InvalidFile

    def run(self):
        self.program_scanner = ProgramScanner(self.program_memory, self.registers)
        self.ops = Operations(self.program_scanner, self.memory, self.registers)

        data_size = self.program_scanner.nextBytes(2)
        self.memory.extend(self.program_scanner.nextBytes(data_size, pack=False))

        print("Main Memory")
        print(self.memory)

        print("Program Memory:")
        print(self.program_memory)

        while 1:
            try:
              opcode = self.program_scanner.nextOpcode()
            except exp.EndOfProgram:
              break
            print('Op: %d' % opcode)
            op = self.ops.fromCode(opcode)
            op()
        print("Main Memory")
        print(self.memory)

        print(self.registers)
