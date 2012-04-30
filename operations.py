from registers import Registers
from utils import unpack_bytes, pack_bytes
import interrupts
from interrupts import Interrupts, codeToInt

codeToOperation = {
  0x0: 'mov_reg_reg',
  0x1: 'mov_reg_mem',
  0x2: 'mov_mem_reg',
  0x3: 'mov_reg_lit',
  0x4: 'add_reg_reg',
  0x5: 'add_reg_lit',
  0x6: 'sub_reg_reg',
  0x7: 'sub_reg_lit',
  0x8: 'mul_reg_reg',
  0x9: 'mul_reg_lit',
  0xa: 'div_reg_reg',
  0xb: 'div_reg_lit',

  0x10: 'jmp_nz',

  0xff: 'int'
}
operationToCode = {codeToOperation[x]: x for x in codeToOperation}

class Operations(object):
    def __init__(self, program_scanner, memory,
                 registers):
        self.program_scanner = program_scanner
        self.memory = memory
        self.registers = registers
        self.interrupts = Interrupts(self.registers, self.memory)

    def fromCode(self, code):
        return getattr(self, codeToOperation[code])

    def mov_reg_reg(self):
        a = self.program_scanner.nextRegister()
        b = self.program_scanner.nextRegister()
        self.registers.set(a, self.registers.get(b))

    def mov_reg_mem(self):
        a = self.program_scanner.nextRegister()
        b = self.program_scanner.nextMemory()
        print(b)
        b = self.memory[b:b + Registers.sizeOf(a)]
        self.registers.set(a, pack_bytes(b))

    def mov_mem_reg(self):
        a = self.program_scanner.nextRegister()
        b = self.program_scanner.nextBytes(2)
        a = unpack_bytes(self.registers.get(a))
        for byte in a:
            self.memory[b] = byte
            b += 1

    def mov_reg_lit(self):
        a = self.program_scanner.nextRegister()
        b = self.program_scanner.nextBytes(Registers.sizeOf(a))
        self.registers.set(a, b)

    def add_reg_reg(self):
        a = self.program_scanner.nextRegister()
        b = self.program_scanner.nextRegister()
        c = self.registers.get(a) + self.registers.get(b)
        self.registers.set(a, c)

    def sub_reg_reg(self):
        a = self.program_scanner.nextRegister()
        b = self.program_scanner.nextRegister()
        c = self.registers.get(a) - self.registers.get(b)
        self.registers.set(a, c)

    def sub_reg_lit(self):
        a = self.program_scanner.nextRegister()
        b = self.program_scanner.nextBytes(Registers.sizeOf(a))
        c = self.registers.get(a) - b
        self.registers.set(a, c)

    def mul_reg_reg(self):
        a = self.program_scanner.nextRegister()
        b = self.program_scanner.nextRegister()
        c = self.registers.get(a) * self.registers.get(b)
        self.registers.set(Registers.nextSize(a), c)

    def jmp_nz(self):
        a = self.program_scanner.nextMemory()
        ax = self.registers.get('ax')
        if ax != 0:
            self.registers.pc = a

    def int(self):
        a = self.program_scanner.nextBytes(1)
        getattr(self.interrupts, codeToInt[a])()
