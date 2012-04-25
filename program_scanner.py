import utils
from registers import Registers
import exceptions as exp

OPCODE_SIZE = 1
REGISTER_SIZE = 1
MEMORY_SIZE = 2

DB_SIZE = 1
DW_SIZE = 2
DD_SIZE = 4

class ProgramScanner(object):
    def __init__(self, memory, registers):
      self.memory = memory
      self.registers = registers

    def nextOpcode(self):
      return self.nextBytes(OPCODE_SIZE)

    def nextRegister(self):
      a = self.nextBytes(REGISTER_SIZE)
      return Registers.codeToName(a)

    def nextMemory(self):
      return self.nextBytes(MEMORY_SIZE)

    def nextBytes(self, size=1, pack=True):
      pc = self.registers.pc

      if pc >= len(self.memory):
          raise exp.EndOfProgram

      byte = self.memory[pc:pc + size]
      self.registers.incrementPC(size)

      if pack is True:
          return utils.pack_bytes(byte)
      return byte
