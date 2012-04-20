from t81.common import utils
from .registers import codeToRegister

OPCODE_SIZE = 1
REGISTER_SIZE = 1

class ProgramScanner(object):
    def __init__(self, memory, registers):
      self.memory = memory
      self.registers = registers

    def pc(self):
      return self.registers.getPC()

    def nextOpcode(self):
      code = self.stringFromSlice(OPCODE_SIZE)
      self.registers.incrementPC()
      return code

    def nextRegister(self):
      reg = self.stringFromSlice(REGISTER_SIZE)
      self.registers.incrementPC()
      return codeToRegister[reg]

    def stringFromSlice(self, slice_size=1):
      byte = self.memory[self.pc():self.pc() + slice_size]
      return utils.pack_bytes(byte)
