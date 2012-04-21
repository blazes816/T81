import utils

codeToName = {
  0x00: 'eax',
  0x01: 'ax',
  0x02: 'ah',
  0x03: 'al',
  0x04: 'ebx',
  0x05: 'bx',
  0x06: 'bh',
  0x07: 'bl',
}

class Registers(object):
    @staticmethod
    def codeToName(code):
        return codeToName[code]

    @staticmethod
    def sizeOf(reg):
        if len(reg) == 3:
            return 4
        elif len(reg) == 2 and reg[-1] == x:
            return 2
        return 1
            


    def __init__(self):
        self.eax = 0
        self.ebx = 0
        self.ecx = 0
        self.edx = 0

        self.pc = 0

        self.registers = {
          'eax': self.eax, 'ebx': self.ebx, 'ecx': self.ecx, 'edx': self.edx,
          'pc': self.pc
        }

        self.registers_available = list(self.registers.keys())

    def incrementPC(self, amount=0x01):
        self.pc = (self.pc + amount)

    def set(self, name, value):
        if name in list(self.registers.keys()):
            self.registers[name] = value
        elif name in [x + y for x in ('a', 'b', 'c', 'd') for y in ('x', 'h', 'l')]:
            print(name)

    def get(self, reg):
        if type(reg) is int:
            reg = self.codeToName(reg)

        if len(reg) == 3:
            print('asdf')
            return self.registers[reg]
        else:
            v = self.registers['e'+reg]

    def __repr__(self):
        return repr(self.registers)
