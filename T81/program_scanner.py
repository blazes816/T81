from functools import reduce

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
      return reduce(lambda x,y: (x << 8) + int(y, 16), byte, 0x0)
