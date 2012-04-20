import utils
from registers import codeToRegister

OPCODE_SIZE = 1
REGISTER_SIZE = 1

class ProgramScanner(object):
    def __init__(self, memory, registers):
      self.memory = memory
      self.registers = registers

    def pc(self):
      return self.registers.get_pc

    def nextOpcode(self):
      code = self.stringFromSlice(OPCODE_SIZE)
      return code

    def nextRegister(self):
      reg = self.stringFromSlice(REGISTER_SIZE)
      return codeToRegister[reg]

    def stringFromSlice(self, slice_size=1):
      byte = self.memory[self.pc():self.pc() + slice_size]
      self.registers.incrementPC(slice_size)
      return utils.pack_bytes(byte)
