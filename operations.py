from registers import Registers
from utils import unpack_bytes

codeToOperation = {
  0x0: 'mov_reg_reg',
  0x1: 'mov_reg_mem',
  0x2: 'mov_mem_reg',
  0x3: 'mov_reg_lit'
}
operationToCode = {codeToOperation[x]: x for x in codeToOperation}

class Operations(object):
    def __init__(self, program_scanner, memory,
                 registers):
        self.program_scanner = program_scanner
        self.memory = memory
        self.registers = registers

    def fromCode(self, code):
        return getattr(self, codeToOperation[code])

    def mov_reg_reg(self):
        a = self.program_scanner.nextRegister()
        b = self.program_scanner.nextRegister()
        self.registers.set(a, self.registers.get(b))

    def mov_reg_mem(self):
        a = self.program_scanner.nextRegister()
        b = self.program_scanner.nextRegister()

    def mov_mem_reg(self):
        a = self.program_scanner.nextRegister()
        b = self.program_scanner.nextBytes(Registers.sizeOf(a))
        a = unpack_bytes(self.registers.get(a))
        for byte in a:
            self.memory[b] = byte
            b += 1

    def mov_reg_lit(self):
        a = self.program_scanner.nextRegister()
        b = self.program_scanner.nextBytes(Registers.sizeOf(a))
        self.registers.set(a, b)
